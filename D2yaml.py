import yaml

def traefik_to_d2(yaml_path):
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    http = config.get('http', {})
    routers = http.get('routers', {})
    services = http.get('services', {})

    d2_lines = [
        "direction: right",
        "vars: {",
        "  d2-config: {",
        "    layout-engine: dagre",
        "    theme: 200",
        "  }",
        "}"
    ]

    # Process Routers and Connections
    for r_name, r_data in routers.items():
        entrypoint = r_data.get('entryPoints', ['web'])[0]
        rule = r_data.get('rule', 'no-rule').replace('`', "'")
        service_name = r_data.get('service')
        middlewares = r_data.get('middlewares', [])

        # Define EntryPoint to Router
        d2_lines.append(f"{entrypoint} -> {r_name}: {rule}")

        # If middlewares exist, route through them
        last_node = r_name
        if middlewares:
            for mid in middlewares:
                d2_lines.append(f"{last_node} -> {mid}")
                d2_lines.append(f"{mid}.shape: parallelogram")
                last_node = mid
        
        # Connect to Service
        d2_lines.append(f"{last_node} -> {service_name}")

        # Detail the Service Backends
        if service_name in services:
            servers = services[service_name].get('loadBalancer', {}).get('servers', [])
            for i, server in enumerate(servers):
                url = server.get('url')
                d2_lines.append(f"{service_name} -> backend_{service_name}_{i}: {url}")
                d2_lines.append(f"backend_{service_name}_{i}.shape: square")

    return "\n".join(d2_lines)

# Run and Print
d2_output = traefik_to_d2('dynamic_conf.yml')
print(d2_output)
