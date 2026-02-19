import re
import hashlib
from datetime import datetime
import os

class EmailAnalysisService:
    """Service for analyzing emails for AI-generated phishing"""
    
    @staticmethod
    def analyze_email(email_data):
        """
        Analyze email for phishing and AI-generation indicators
        Returns risk score and key indicators
        """
        risk_score = 0.0
        indicators = []
        
        # Check for generic greetings (common in AI phishing)
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        
        generic_greetings = ['dear user', 'dear customer', 'hello', 'greetings']
        for greeting in generic_greetings:
            if greeting in body[:100]:
                risk_score += 0.15
                indicators.append('generic_greeting')
                break
        
        # Check for urgency manipulation (common in phishing)
        urgency_keywords = ['urgent', 'immediate', 'verify', 'confirm', 'validate', 'immediately', 'asap']
        urgency_count = sum(1 for kw in urgency_keywords if kw in body)
        if urgency_count > 0:
            risk_score += min(0.2, urgency_count * 0.05)
            indicators.append('urgency_manipulation')
        
        # Check for suspicious links
        link_pattern = r'https?://[^\s)]+'
        links = re.findall(link_pattern, body)
        suspicious_links = [l for l in links if any(x in l.lower() for x in ['verify', 'confirm', 'update', 'secure'])]
        if suspicious_links:
            risk_score += 0.25
            indicators.append('suspicious_links')
        
        # Check for sender spoofing
        sender = email_data.get('from', '')
        if 'noreply' in sender.lower() or len(sender.split('@')) != 2:
            risk_score += 0.1
            indicators.append('sender_spoofing')
        
        # Check for credential requests
        cred_keywords = ['password', 'verify account', 'confirm identity', 'login', 'authenticate']
        if any(kw in body.lower() for kw in cred_keywords):
            risk_score += 0.2
            indicators.append('credential_request')
        
        # Normalize score to 0-100
        ai_probability = min(88, int(risk_score * 100))
        
        return {
            'risk_score': min(100, int(risk_score * 100)),
            'ai_probability': ai_probability,
            'indicators': list(set(indicators)),
            'is_phishing': ai_probability > 50,
            'threat_level': 'critical' if ai_probability > 75 else 'high' if ai_probability > 50 else 'medium' if ai_probability > 25 else 'low'
        }
    
    @staticmethod
    def check_credential_exposure(email_address):
        """Check if email has been found in dark web leaks"""
        # Mock implementation - in production would query breach databases
        exposed = hashlib.md5(email_address.encode()).hexdigest().startswith('a')
        
        if exposed:
            return {
                'exposed': True,
                'databases': ['Adobe', 'LinkedIn', 'MySpace'],
                'leaked_count': 3,
                'risk': 'high'
            }
        else:
            return {
                'exposed': False,
                'databases': [],
                'leaked_count': 0,
                'risk': 'low'
            }

class URLAnalysisService:
    """Service for analyzing URLs for phishing and spoofing"""
    
    @staticmethod
    def analyze_url(url):
        """Analyze URL for phishing indicators"""
        risk_score = 0.0
        indicators = []
        
        # Check for suspicious TLD
        if url.endswith('.tk') or url.endswith('.ml') or url.endswith('.ga'):
            risk_score += 0.15
            indicators.append('suspicious_tld')
        
        # Check for typosquatting
        legitimate_domains = ['paypal.com', 'apple.com', 'amazon.com', 'microsoft.com', 'google.com']
        for domain in legitimate_domains:
            if domain[:-4] in url.lower():  # Remove .com
                similarity = 94 if url.count('-') > 0 or url.count('0') > 0 else 85
                risk_score += 0.3
                indicators.append('typosquatting')
                break
        
        # Check for newly registered domain indicator
        if 'paypal-verify' in url or 'verify-account' in url:
            risk_score += 0.25
            indicators.append('newly_registered')
        
        # Check for IP address instead of domain
        if re.match(r'https?://\d+\.\d+\.\d+\.\d+', url):
            risk_score += 0.2
            indicators.append('ip_address')
        
        # Check for suspicious subdomains
        if url.count('.') > 3:
            risk_score += 0.1
            indicators.append('unusual_subdomain')
        
        phishing_score = min(95, int(risk_score * 100))
        
        return {
            'url': url,
            'phishing_risk_score': phishing_score,
            'domain_age': 'newly_registered',
            'domain_registrar': 'GoDaddy',
            'similarity_to_legitimate': 94 if 'paypal' in url else 65,
            'indicators': list(set(indicators)),
            'ssl_valid': False,
            'is_phishing': phishing_score > 70,
            'threat_level': 'critical' if phishing_score > 80 else 'high' if phishing_score > 60 else 'medium'
        }

class FileAnalysisService:
    """Service for analyzing files for malware"""
    
    @staticmethod
    def analyze_file(filename, file_hash):
        """Analyze file using mock malware indicators"""
        indicators = []
        risk_score = 0.0
        
        # Check suspicious extensions
        suspicious_exts = ['.exe', '.bat', '.cmd', '.scr', '.vbs', '.js', '.app', '.dmg']
        if any(filename.lower().endswith(ext) for ext in suspicious_exts):
            risk_score += 0.3
            indicators.append('executable_extension')
        
        # Check for double extensions (common malware trick)
        if filename.count('.') > 1:
            risk_score += 0.2
            indicators.append('double_extension')
        
        # Check for obfuscated macros (macro analysis simulation)
        if 'macro' in filename.lower() or filename.lower().endswith(('.docm', '.xlsm')):
            risk_score += 0.15
            indicators.append('obfuscated_macros')
        
        # Mock VirusTotal-like results
        threat_level = 'malware' if risk_score > 0.3 else 'suspicious' if risk_score > 0.1 else 'clean'
        vendors_detecting = int(risk_score * 72) if risk_score > 0.2 else 0
        
        return {
            'filename': filename,
            'file_hash': file_hash,
            'threat_level': threat_level,
            'risk_score': min(100, int(risk_score * 100)),
            'vendors_detecting': vendors_detecting,
            'total_vendors': 71,
            'indicators': list(set(indicators)),
            'behavioral_analysis': {
                'registry_modifications': risk_score > 0.25,
                'network_calls': risk_score > 0.2,
                'file_operations': risk_score > 0.15,
                'process_injection': risk_score > 0.3
            },
            'mitre_techniques': ['T1547.001', 'T1566.001', 'T1204.002'] if risk_score > 0.3 else []
        }

class AudioAnalysisService:
    """Service for detecting deepfake audio"""
    
    @staticmethod
    def analyze_audio(audio_data):
        """Analyze audio for deepfake indicators"""
        # Mock MFCC-based analysis
        synthetic_probability = 92.4
        
        return {
            'synthetic_probability': synthetic_probability,
            'is_deepfake': synthetic_probability > 80,
            'confidence': 0.94,
            'model_used': 'Parallel WaveGAN with HiFi-GAN vocoder',
            'mfcc_features': {
                'spectral_centroid': 'high_variance',
                'chroma_shifts': 'detected',
                'zero_crossing_rate': 'anomalous'
            },
            'call_metadata': {
                'origin': 'VoIP',
                'duration_seconds': 180,
                'network_jitter': 'moderate'
            },
            'threat_indicators': [
                'non_human_artifacts',
                'rhythmic_discontinuity',
                'processing_artifacts'
            ]
        }

class PromptInjectionService:
    """Service for testing LLM vulnerabilities"""
    
    @staticmethod
    def test_prompt_injection(prompt, model='mistral', attack_type='jailbreaking'):
        """Test prompt against LLM for injection vulnerabilities"""
        
        # Simulate prompt injection detection
        dangerous_patterns = ['ignore previous', 'forget', 'override', 'bypass', 'disregard']
        detected_patterns = [p for p in dangerous_patterns if p.lower() in prompt.lower()]
        
        success_rate = len(detected_patterns) * 0.2 if detected_patterns else 0.05
        
        return {
            'prompt': prompt,
            'model': model,
            'attack_type': attack_type,
            'success_rate': min(32, int(success_rate * 100)),
            'blocked_rate': max(68, 100 - int(success_rate * 100)),
            'detected_patterns': detected_patterns,
            'guardrails_triggered': len(detected_patterns) > 0,
            'data_leak_detected': False,
            'mitre_techniques': ['T1027.005', 'T1566.002'] if detected_patterns else [],
            'recommendation': 'Prompt blocked by content filter' if detected_patterns else 'No injection detected'
        }

class DarkWebService:
    """Service for monitoring dark web exposure"""
    
    @staticmethod
    def get_credential_exposure(email):
        """Get credential exposure from dark web monitoring"""
        # Mock dark web data
        exposed_credentials = [
            {'username': 'j.smith', 'source': 'BreachForums', 'date': '2025-11-15', 'risk': 'HIGH'},
            {'username': 'admin_dev', 'source': 'Exploit.in', 'date': '2025-10-20', 'risk': 'HIGH'},
            {'username': 'm.garcia', 'source': 'XSS.is', 'date': '2025-09-10', 'risk': 'MEDIUM'},
        ]
        
        return {
            'email': email,
            'total_exposed': 2481,
            'credentials_found': exposed_credentials[:2] if email.startswith('j') else [],
            'exposure_sources': ['BreachForums', 'Exploit.in', 'Paste Sites'],
            'risk_level': 'HIGH' if exposed_credentials else 'LOW'
        }

class RiskScoringService:
    """Service for calculating overall risk posture"""
    
    @staticmethod
    def calculate_risk_posture():
        """Calculate overall system risk posture"""
        return {
            'overall_score': 16,  # 0-100, lower is better
            'risk_level': 'LOW',
            'credentials_exposed': 2481,
            'phishing_sites': 45200,
            'model_jailbreaks': 12,
            'deepfakes_detected': 34,
            'incidents_active': 7,
            'sla_compliance': 100.0,
            'mttr_hours': 4.2
        }
