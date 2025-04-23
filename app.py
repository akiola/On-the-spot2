from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'onthespottransfer_secret_key'

# Add a context processor to inject the current year into all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Current exchange rates as of April 2025 (for demo purposes)
EXCHANGE_RATES = {
    'NGN': 85.42,  # Nigerian Naira
    'USD': 12.76,  # US Dollar
    'EUR': 11.83,  # Euro (France)
    'CAD': 9.45,   # Canadian Dollar
}

# Transfer fees (percentage)
TRANSFER_FEES = {
    'NGN': 2.5,
    'USD': 3.0,
    'EUR': 3.0,
    'CAD': 3.0,
}

# Country codes to full names
COUNTRY_NAMES = {
    'NGN': 'Nigeria',
    'USD': 'United States',
    'EUR': 'France',
    'CAD': 'Canada',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html', 
                           exchange_rates=EXCHANGE_RATES, 
                           transfer_fees=TRANSFER_FEES,
                           country_names=COUNTRY_NAMES)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        try:
            # Get and validate form data
            amount_str = request.form.get('amount', '')
            currency = request.form.get('currency')
            recipient_name = request.form.get('recipient_name')
            recipient_account = request.form.get('recipient_account')
            payment_method = request.form.get('payment_method')
            
            # Validate required fields
            if not all([amount_str, currency, recipient_name, recipient_account, payment_method]):
                flash('Please fill out all required fields.', 'error')
                return render_template('transfer.html', 
                                      exchange_rates=EXCHANGE_RATES, 
                                      transfer_fees=TRANSFER_FEES,
                                      country_names=COUNTRY_NAMES)
                
            # Validate amount is a valid number
            try:
                amount = float(amount_str)
                if amount <= 0:
                    flash('Amount must be greater than zero.', 'error')
                    return render_template('transfer.html', 
                                          exchange_rates=EXCHANGE_RATES, 
                                          transfer_fees=TRANSFER_FEES,
                                          country_names=COUNTRY_NAMES)
            except ValueError:
                flash('Invalid amount. Please enter a valid number.', 'error')
                return render_template('transfer.html', 
                                      exchange_rates=EXCHANGE_RATES, 
                                      transfer_fees=TRANSFER_FEES,
                                      country_names=COUNTRY_NAMES)
            
            # Validate currency is supported
            if currency not in EXCHANGE_RATES:
                flash('Invalid currency selected.', 'error')
                return render_template('transfer.html', 
                                      exchange_rates=EXCHANGE_RATES, 
                                      transfer_fees=TRANSFER_FEES,
                                      country_names=COUNTRY_NAMES)
            
            # Calculate exchange amount and fee
            exchange_rate = EXCHANGE_RATES.get(currency, 0)
            fee_percentage = TRANSFER_FEES.get(currency, 0)
            fee_amount = (amount * fee_percentage) / 100
            total_amount = amount + fee_amount
            received_amount = amount * exchange_rate
            
            # Store transfer details in session for confirmation
            session['transfer'] = {
                'amount': amount,
                'currency': currency,
                'country': COUNTRY_NAMES.get(currency),
                'recipient_name': recipient_name,
                'recipient_account': recipient_account,
                'payment_method': payment_method,
                'exchange_rate': exchange_rate,
                'fee_amount': fee_amount,
                'total_amount': total_amount,
                'received_amount': received_amount,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'transaction_id': f"OTST-{datetime.now().strftime('%y%m%d%H%M%S')}"
            }
            
            return redirect(url_for('confirm'))
            
        except Exception as e:
            # Handle any unexpected errors
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template('transfer.html', 
                                  exchange_rates=EXCHANGE_RATES, 
                                  transfer_fees=TRANSFER_FEES,
                                  country_names=COUNTRY_NAMES)
    
    return render_template('transfer.html', 
                           exchange_rates=EXCHANGE_RATES, 
                           transfer_fees=TRANSFER_FEES,
                           country_names=COUNTRY_NAMES)

@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    transfer_data = session.get('transfer', {})
    
    if not transfer_data:
        flash('No transfer data found. Please start a new transfer.', 'error')
        return redirect(url_for('transfer'))
    
    if request.method == 'POST':
        # In a real app, this would process the payment
        # For demo, just show success
        return redirect(url_for('success'))
    
    return render_template('confirm.html', transfer=transfer_data)

@app.route('/success')
def success():
    transfer_data = session.get('transfer', {})
    
    if not transfer_data:
        flash('No transfer data found. Please start a new transfer.', 'error')
        return redirect(url_for('transfer'))
    
    # Clear transfer data from session after successful transfer
    # session.pop('transfer', None)
    
    return render_template('success.html', transfer=transfer_data)

@app.route('/mobile_payment', methods=['GET', 'POST'])
def mobile_payment():
    transfer_data = session.get('transfer', {})
    
    if not transfer_data:
        flash('No transfer data found. Please start a new transfer.', 'error')
        return redirect(url_for('transfer'))
    
    if request.method == 'POST':
        # Process mobile payment (demo)
        phone = request.form.get('phone')
        network = request.form.get('network')
        
        # Basic validation
        if not phone or not network:
            flash('Please provide all required information.', 'error')
            return render_template('mobile_payment.html', transfer=transfer_data)
        
        try:
            # In a real app, this would integrate with mobile money API
            # For demo, just continue to success (simulating success case)
            flash(f'Payment request sent to {phone} on {network} network', 'success')
            return redirect(url_for('success'))
        except Exception as e:
            # Handle any potential payment processing errors
            flash(f'Payment processing error: {str(e)}', 'error')
            return render_template('mobile_payment.html', transfer=transfer_data)
    
    return render_template('mobile_payment.html', transfer=transfer_data)

@app.route('/card_payment', methods=['GET', 'POST'])
def card_payment():
    transfer_data = session.get('transfer', {})
    
    if not transfer_data:
        flash('No transfer data found. Please start a new transfer.', 'error')
        return redirect(url_for('transfer'))
    
    if request.method == 'POST':
        # Process card payment (demo)
        # Basic validation
        required_fields = ['card_name', 'card_number', 'expiry_date', 'cvv']
        form_data = {field: request.form.get(field) for field in required_fields}
        
        # Check for missing fields
        if not all(form_data.values()):
            flash('Please fill out all credit card details.', 'error')
            return render_template('card_payment.html', transfer=transfer_data)
        
        try:
            # In a real app, this would integrate with payment gateway
            # For demo, just continue to success
            flash('Card payment processed successfully', 'success')
            return redirect(url_for('success'))
        except Exception as e:
            # Handle any potential payment processing errors
            flash(f'Payment processing error: {str(e)}', 'error')
            return render_template('card_payment.html', transfer=transfer_data)
    
    return render_template('card_payment.html', transfer=transfer_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)