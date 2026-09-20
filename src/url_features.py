"""
URL Feature Extraction Module
Extracts lexical, structural, syntactic, and security indicators from a raw URL.
"""

from urllib.parse import urlparse
import ipaddress
import re
import pandas as pd


URL_FEATURE_COLUMNS = [
    "url_length",
    "domain_length",
    "path_length",
    "num_digits",
    "num_letters",
    "num_dots",
    "num_hyphens",
    "num_slashes",
    "num_at",
    "num_question_marks",
    "num_equals",
    "num_percent",
    "num_special_chars",
    "has_at",
    "has_https",
    "has_ip",
    "num_query_params",
    "num_subdomains",
    "suspicious_keyword_count"
]


def extract_url_features(url: str) -> dict:
    """
    Extracts numerical and categorical features from a given URL string.
    """
    raw_url = str(url).strip()
    if not (raw_url.startswith("http://") or raw_url.startswith("https://")):
        parsed = urlparse("http://" + raw_url)
        is_https = 0
    else:
        parsed = urlparse(raw_url)
        is_https = 1 if parsed.scheme.lower() == "https" else 0

    hostname = parsed.netloc if parsed.netloc else parsed.path.split("/")[0]
    hostname_clean = hostname.split(":")[0]  # remove port if present
    path = parsed.path
    query = parsed.query

    # IP address check
    has_ip = 0
    try:
        ipaddress.ip_address(hostname_clean)
        has_ip = 1
    except ValueError:
        has_ip = 0

    # Subdomain count
    domain_parts = hostname_clean.split(".")
    subdomains_count = max(len(domain_parts) - 2, 0)

    # Suspicious keywords
    keywords = ["login", "verify", "secure", "account", "update", "banking", "signin", "password", "wallet", "confirm"]
    suspicious_count = sum(1 for kw in keywords if kw in raw_url.lower())

    features = {
        "url_length": len(raw_url),
        "domain_length": len(hostname_clean),
        "path_length": len(path),
        "num_digits": sum(c.isdigit() for c in raw_url),
        "num_letters": sum(c.isalpha() for c in raw_url),
        "num_dots": raw_url.count("."),
        "num_hyphens": raw_url.count("-"),
        "num_slashes": raw_url.count("/"),
        "num_at": raw_url.count("@"),
        "num_question_marks": raw_url.count("?"),
        "num_equals": raw_url.count("="),
        "num_percent": raw_url.count("%"),
        "num_special_chars": sum(not c.isalnum() for c in raw_url),
        "has_at": int("@" in raw_url),
        "has_https": is_https,
        "has_ip": has_ip,
        "num_query_params": len(query.split("&")) if query else 0,
        "num_subdomains": subdomains_count,
        "suspicious_keyword_count": suspicious_count,
    }

    return features


def extract_features_df(urls: list) -> pd.DataFrame:
    data = [extract_url_features(u) for u in urls]
    return pd.DataFrame(data)


if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.1/update-account/bank-verify-secure"
    ]
    for u in test_urls:
        print(f"\nFeatures for {u}:")
        for k, v in extract_url_features(u).items():
            print(f"  {k}: {v}")
