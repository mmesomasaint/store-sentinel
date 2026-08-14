# app/core/security.py
import socket
import ipaddress
from urllib.parse import urlparse
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != settings.API_KEY.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header."
        )
    return api_key

def validate_url_against_ssrf(target_url: str) -> bool:
    """
    Resolves domain to IP and rejects requests targeting private/internal network ranges.
    """
    try:
        parsed = urlparse(target_url)
        hostname = parsed.hostname
        if not hostname:
            return False
            
        ip_addr = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip_addr)
        
        # Reject private, loopback, or multicast IPs
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            return False
        return True
    except Exception:
        return False
