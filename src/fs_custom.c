#include "lwip/apps/fs.h"
#include "html_data.h"
#include <string.h>

#define INDEX_HTML "/"
#define INDEX_HTML_FULL "/index.html"

int fs_open_custom(struct fs_file *file, const char *name) {
    if (strcmp(name, INDEX_HTML) == 0 || strcmp(name, INDEX_HTML_FULL) == 0) {
        file->data = (const char *)html_data;
        file->len = html_data_len;
        file->index = html_data_len;
        file->flags = FS_FILE_FLAGS_HEADER_INCLUDED | FS_FILE_FLAGS_CUSTOM;
        return 1;
    }
    return 0; // Not found
}

void fs_close_custom(struct fs_file *file) {
    // Nothing to do
}

#if LWIP_HTTPD_FS_ASYNC_READ
int fs_read_custom(struct fs_file *file, char *buffer, int count, fs_wait_cb callback_fn, void *callback_arg) {
    return FS_READ_EOF;
}
#else
int fs_read_custom(struct fs_file *file, char *buffer, int count) {
    return FS_READ_EOF;
}
#endif
