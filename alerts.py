import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Alert history storage
alert_history = []

def get_alert_thresholds():
    """Get configurable alert thresholds from environment or defaults"""
    return {
        'heart_rate_high': int(os.getenv('HEART_RATE_HIGH', 100)),
        'heart_rate_low': int(os.getenv('HEART_RATE_LOW', 50)),
        'blood_oxygen_low': int(os.getenv('BLOOD_OXYGEN_LOW', 92)),
        'temperature_high': float(os.getenv('TEMPERATURE_HIGH', 38.0)),
        'temperature_low': float(os.getenv('TEMPERATURE_LOW', 35.5)),
        'respiration_high': int(os.getenv('RESPIRATION_HIGH', 25)),
        'respiration_low': int(os.getenv('RESPIRATION_LOW', 10)),
    }

def check_vitals_for_alerts(vitals, user_id="Unknown"):
    """Check vitals against thresholds and return list of alerts"""
    thresholds = get_alert_thresholds()
    alerts = []
    
    # Check heart rate
    if 'heart_rate' in vitals:
        hr = vitals['heart_rate']
        if hr > thresholds['heart_rate_high']:
            alerts.append({
                'severity': 'HIGH',
                'type': 'Tachycardia',
                'message': f'Heart rate {hr} BPM exceeds safe threshold ({thresholds["heart_rate_high"]} BPM)',
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            })
        elif hr < thresholds['heart_rate_low']:
            alerts.append({
                'severity': 'HIGH',
                'type': 'Bradycardia',
                'message': f'Heart rate {hr} BPM below safe threshold ({thresholds["heart_rate_low"]} BPM)',
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            })
    
    # Check blood oxygen
    if 'blood_oxygen' in vitals:
        o2 = vitals['blood_oxygen']
        if o2 < thresholds['blood_oxygen_low']:
            alerts.append({
                'severity': 'CRITICAL',
                'type': 'Hypoxia',
                'message': f'Blood oxygen {o2}% is critically low (threshold: {thresholds["blood_oxygen_low"]}%)',
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            })
    
    # Check temperature
    if 'temperature' in vitals:
        temp = vitals['temperature']
        if temp > thresholds['temperature_high']:
            alerts.append({
                'severity': 'MEDIUM',
                'type': 'Fever',
                'message': f'Temperature {temp}°C indicates potential fever (threshold: {thresholds["temperature_high"]}°C)',
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            })
        elif temp < thresholds['temperature_low']:
            alerts.append({
                'severity': 'HIGH',
                'type': 'Hypothermia',
                'message': f'Temperature {temp}°C is dangerously low (threshold: {thresholds["temperature_low"]}°C)',
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            })
    
    # Check respiration
    if 'respiration_rate' in vitals:
        resp = vitals['respiration_rate']
        if resp > thresholds['respiration_high']:
            alerts.append({
                'severity': 'MEDIUM',
                'type': 'Tachypnea',
                'message': f'Respiration rate {resp} breaths/min is elevated (threshold: {thresholds["respiration_high"]})',
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            })
        elif resp < thresholds['respiration_low']:
            alerts.append({
                'severity': 'HIGH',
                'type': 'Bradypnea',
                'message': f'Respiration rate {resp} breaths/min is too low (threshold: {thresholds["respiration_low"]})',
                'user_id': user_id,
                'timestamp': datetime.now().isoformat()
            })
    
    # Store in history
    for alert in alerts:
        alert_history.append(alert)
    
    return alerts

def send_email_alert(to_email, subject, message):
    """Send email alert via SMTP"""
    enable_real_alerts = os.getenv('ENABLE_REAL_ALERTS', 'false').lower() == 'true'
    
    if not enable_real_alerts:
        # Simulation mode
        print(f"\n📧 [EMAIL ALERT SIMULATION]")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print("=" * 60)
        return True
    
    # Real email sending (requires SMTP configuration)
    try:
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_email = os.getenv('SMTP_EMAIL')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not all([smtp_server, smtp_email, smtp_password]):
            print("SMTP not configured. Using simulation mode.")
            return send_email_alert(to_email, subject, message)  # Fallback to simulation
        
        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email alert sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def send_sms_alert(phone_number, message):
    """Send SMS alert (Twilio simulation)"""
    enable_real_alerts = os.getenv('ENABLE_REAL_ALERTS', 'false').lower() == 'true'
    
    if not enable_real_alerts:
        # Simulation mode
        print(f"\n📱 [SMS ALERT SIMULATION]")
        print(f"To: {phone_number}")
        print(f"Message: {message}")
        print("=" * 60)
        return True
    
    # Real SMS sending would use Twilio or similar service
    print("SMS alerts require Twilio configuration. Using simulation mode.")
    return send_sms_alert(phone_number, message)

def process_alerts_and_notify(vitals, user_id, email=None, phone=None):
    """Check vitals, generate alerts, and send notifications"""
    alerts = check_vitals_for_alerts(vitals, user_id)
    
    for alert in alerts:
        if email:
            subject = f"⚠️ Health Alert: {alert['type']} - {alert['severity']}"
            send_email_alert(email, subject, alert['message'])
        
        if phone and alert['severity'] in ['HIGH', 'CRITICAL']:
            send_sms_alert(phone, f"URGENT: {alert['message']}")
    
    return alerts

def get_alert_history(user_id=None, limit=50):
    """Get alert history, optionally filtered by user"""
    if user_id:
        user_alerts = [a for a in alert_history if a['user_id'] == user_id]
        return user_alerts[-limit:]
    return alert_history[-limit:]

def clear_alert_history():
    """Clear all alert history"""
    global alert_history
    alert_history = []
