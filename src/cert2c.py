import os

def convert(filename, var_name, out_file):
    with open(filename, 'rb') as f:
        data = f.read()
    
    # mbedtls requires a null-terminated string for PEM certificates and keys
    data += b'\0'
    
    out_file.write(f'const unsigned char {var_name}[] = {{\n')
    for i, b in enumerate(data):
        out_file.write(f'0x{b:02x}, ')
        if (i + 1) % 12 == 0:
            out_file.write('\n')
    out_file.write('\n};\n')
    out_file.write(f'const unsigned int {var_name}_len = {len(data)};\n\n')

with open('cert_data.h', 'w') as f:
    f.write('#ifndef _CERT_DATA_H_\n#define _CERT_DATA_H_\n\n')
    convert('cert.pem', 'cert_pem', f)
    convert('key.pem', 'key_pem', f)
    f.write('#endif\n')
