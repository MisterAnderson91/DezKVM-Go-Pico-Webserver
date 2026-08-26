import sys

def convert(filename, out_filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    with open(out_filename, 'w') as f:
        f.write('#ifndef _HTML_DATA_H_\n#define _HTML_DATA_H_\n\n')
        f.write('const unsigned char index_html[] = {\n')
        for i, b in enumerate(data):
            f.write(f'0x{b:02x}, ')
            if (i + 1) % 12 == 0:
                f.write('\n')
        f.write('\n};\n')
        f.write(f'const unsigned int index_html_len = {len(data)};\n\n')
        f.write('#endif\n')

if __name__ == '__main__':
    convert('index.html', 'html_data.h')
