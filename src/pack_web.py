import os
import sys
import gzip

def get_mime_type(path):
    if path.endswith('.html'): return 'text/html'
    if path.endswith('.js'): return 'application/javascript'
    if path.endswith('.css'): return 'text/css'
    if path.endswith('.svg'): return 'image/svg+xml'
    if path.endswith('.png'): return 'image/png'
    return 'application/octet-stream'

def convert(web_dir, out_filename):
    files = []
    for root, dirs, filenames in os.walk(web_dir):
        for filename in filenames:
            if filename.startswith('.'): continue
            path = os.path.join(root, filename)
            web_path = '/' + os.path.relpath(path, web_dir).replace('\\', '/')
            if web_path == '/index.html':
                web_path = '/' # also map to root
            with open(path, 'rb') as f:
                data = f.read()
            files.append((web_path, path, data))

    with open(out_filename, 'w') as f:
        f.write('#ifndef _HTML_DATA_H_\n#define _HTML_DATA_H_\n\n')
        f.write('#include <stddef.h>\n\n')
        f.write('typedef struct {\n')
        f.write('    const char* path;\n')
        f.write('    const unsigned char* data;\n')
        f.write('    size_t length;\n')
        f.write('} web_file_t;\n\n')
        
        for i, (web_path, path, data) in enumerate(files):
            mime_type = get_mime_type(path)
            
            if path.endswith('.html') or path.endswith('.js') or path.endswith('.css'):
                data = gzip.compress(data)
                encoding_header = "Content-Encoding: gzip\r\n"
            else:
                encoding_header = ""

            content_length = len(data)
            header = f"HTTP/1.0 200 OK\r\nContent-Type: {mime_type}\r\n{encoding_header}Content-Length: {content_length}\r\nConnection: close\r\n\r\n".encode('utf-8')
            full_data = header + data
            
            f.write(f'const unsigned char file_data_{i}[] = {{\n')
            for j, b in enumerate(full_data):
                f.write(f'0x{b:02x}, ')
                if (j + 1) % 16 == 0: f.write('\n')
            f.write('\n};\n')
            
        f.write('const web_file_t web_files[] = {\n')
        for i, (web_path, path, data) in enumerate(files):
            if web_path == '/':
                f.write(f'    {{"/", file_data_{i}, sizeof(file_data_{i})}},\n')
                f.write(f'    {{"/index.html", file_data_{i}, sizeof(file_data_{i})}},\n')
            else:
                f.write(f'    {{"{web_path}", file_data_{i}, sizeof(file_data_{i})}},\n')
        f.write('};\n')
        
        num_mappings = len(files) + (1 if any(w == '/' for w, p, d in files) else 0)
        f.write(f'const int num_web_files = {num_mappings};\n\n')
        f.write('#endif\n')

if __name__ == '__main__':
    convert('web', 'html_data.h')
