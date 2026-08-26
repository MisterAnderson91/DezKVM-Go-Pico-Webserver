#include "lwip/apps/fs.h"
#include <string.h>
#include "html_data.h"

int fs_open_custom(struct fs_file *file, const char *name) {
  for (int i = 0; i < num_web_files; i++) {
      if (strcmp(name, web_files[i].path) == 0) {
          file->data = (const char *)web_files[i].data;
          file->len = web_files[i].length;
          file->index = file->len;
          file->flags = FS_FILE_FLAGS_HEADER_INCLUDED;
          return 1;
      }
  }
  return 0;
}

void fs_close_custom(struct fs_file *file) {
  (void)file;
}

int fs_read_custom(struct fs_file *file, char *buffer, int count) {
  (void)file;
  (void)buffer;
  (void)count;
  return 0; // Everything is handled in memory via file->data
}
