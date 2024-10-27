def get_proxies(proxy_type, host_name, port, login=None, password=None):
    if proxy_type in ["HttpProxy", "Socks5Proxy"]:
        proxy_address = f"{host_name}:{port}"
        
        if login and password:
            proxy_address = f"{login}:{password}@{proxy_address}"
        
        proxy_type = "http" if proxy_type == "HttpProxy" else "socks5"
        return {
            "http": f"{proxy_type}://{proxy_address}",
            "https": f"{proxy_type}://{proxy_address}"
        }
    else:
        return {}