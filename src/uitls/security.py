# src/utils/security.py
import hashlib
import os
import logging
from typing import Optional, Dict, Any
import tempfile
from config import Config

logger = logging.getLogger(__name__)

class SecurityManager:
    def __init__(self):
        """Initialize security manager"""
        self.max_file_size = Config.MAX_FILE_SIZE
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS
        self.sensitive_patterns = [
            r'\b\d{12}\b',  # Aadhaar-like numbers
            r'\b\d{10}\b',  # Phone numbers
            r'\b[A-Z]{5}\d{4}[A-Z]\b',  # PAN-like patterns
            r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card-like numbers
        ]
    
    def validate_file_upload(self, uploaded_file) -> bool:
        """Validate uploaded file for security"""
        try:
            # Check file size
            if uploaded_file.size > self.max_file_size:
                logger.warning(f"File too large: {uploaded_file.size} bytes")
                return False
            
            # Check file extension
            file_extension = f".{uploaded_file.name.split('.')[-1].lower()}"
            if file_extension not in self.allowed_extensions:
                logger.warning(f"Invalid file extension: {file_extension}")
                return False
            
            # Basic content validation (check for executable content)
            file_content = uploaded_file.read()
            uploaded_file.seek(0)  # Reset file pointer
            
            if self._contains_executable_content(file_content):
                logger.warning("File contains potentially executable content")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating file upload: {e}")
            return False
    
    def sanitize_text(self, text: str) -> str:
        """Sanitize text by removing or masking sensitive information"""
        try:
            sanitized_text = text
            
            # Mask potential sensitive patterns
            import re
            for pattern in self.sensitive_patterns:
                sanitized_text = re.sub(pattern, '[REDACTED]', sanitized_text)
            
            return sanitized_text
            
        except Exception as e:
            logger.error(f"Error sanitizing text: {e}")
            return text
    
    def generate_session_id(self) -> str:
        """Generate secure session ID"""
        return hashlib.sha256(os.urandom(32)).hexdigest()
    
    def hash_content(self, content: str) -> str:
        """Generate hash of content for integrity checking"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _contains_executable_content(self, content: bytes) -> bool:
        """Check if content contains potentially executable material"""
        # Check for common executable file signatures
        executable_signatures = [
            b'MZ',  # Windows PE
            b'\x7fELF',  # Linux ELF
            b'\xfe\xed\xfa',  # Mach-O
            b'<script',  # JavaScript
            b'<?php',  # PHP
        ]
        
        for signature in executable_signatures:
            if signature in content[:1024]:  # Check first 1KB
                return True
        
        return False
    
    def validate_query(self, query: str) -> Dict[str, Any]:
        """Validate user query for security and appropriateness"""
        validation_result = {
            'is_valid': True,
            'warnings': [],
            'sanitized_query': query
        }
        
        try:
            # Check for potential injection attempts
            suspicious_patterns = [
                r'<script.*?</script>',
                r'javascript:',
                r'on\w+\s*=',
                r'eval\s*\(',
                r'exec\s*\(',
            ]
            
            import re
            query_lower = query.lower()
            
            for pattern in suspicious_patterns:
                if re.search(pattern, query_lower):
                    validation_result['warnings'].append(f"Suspicious pattern detected: {pattern}")
            
            # Check query length
            if len(query) > 10000:  # Limit query length
                validation_result['warnings'].append("Query too long")
                validation_result['sanitized_query'] = query[:10000]
            
            # Sanitize the query
            validation_result['sanitized_query'] = self.sanitize_text(query)
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating query: {e}")
            validation_result['is_valid'] = False
            validation_result['warnings'].append(f"Validation error: {str(e)}")
            return validation_result
    
    def secure_temp_file(self, content: bytes, suffix: str = '.tmp') -> str:
        """Create secure temporary file"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            # Set restrictive permissions
            os.chmod(tmp_file_path, 0o600)  # Read/write for owner only
            
            return tmp_file_path
            
        except Exception as e:
            logger.error(f"Error creating secure temp file: {e}")
            raise
    
    def cleanup_temp_file(self, file_path: str) -> bool:
        """Securely cleanup temporary file"""
        try:
            if os.path.exists(file_path):
                # Overwrite file content before deletion (basic secure delete)
                file_size = os.path.getsize(file_path)
                with open(file_path, 'r+b') as f:
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
                
                os.unlink(file_path)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error cleaning up temp file: {e}")
            return False
    
    def audit_log(self, action: str, details: Dict[str, Any] = None) -> None:
        """Log security-relevant actions"""
        try:
            if Config.ENABLE_LOGGING:
                log_entry = {
                    'action': action,
                    'timestamp': logger.time.strftime('%Y-%m-%d %H:%M:%S'),
                    'details': details or {}
                }
                
                # Don't log personal data
                if not Config.LOG_PERSONAL_DATA:
                    # Remove potentially sensitive information
                    if 'content' in log_entry['details']:
                        log_entry['details']['content'] = '[REDACTED]'
                
                logger.info(f"Security Audit: {log_entry}")
                
        except Exception as e:
            logger.error(f"Error in audit logging: {e}")