#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/types.h>

#define SIZE 5
#define AREA SIZE *SIZE
#define SCRORE_SIZE SIZE * 2 + 2
#define MAX_INDEX SIZE - 1

extern uint8_t *init_board() { return calloc(AREA, sizeof(uint8_t)); }
// rrrrrcccccdd
// uldr first
extern bool *init_scores() { return calloc(SCRORE_SIZE, sizeof(bool)); }
extern bool *init_cell_selector() { return calloc(SCRORE_SIZE, sizeof(bool)); }
extern bool *init_field_selector() { return calloc(AREA, sizeof(bool)); }

bool check(uint8_t x, uint8_t y, uint8_t *board,
           uint8_t (*function)(uint8_t, uint8_t, uint8_t)) {
  for (int i = 0; i < SIZE; i++) {
    if (board[function(x, y, i)] < 128) {
      return false;
    }
  }
  return true;
}

uint8_t x_index(uint8_t x, uint8_t y, uint8_t i) { return x * SIZE + i; }
uint8_t y_index(uint8_t x, uint8_t y, uint8_t i) { return i * SIZE + y; }
uint8_t uldr_index(uint8_t x, uint8_t y, uint8_t i) { return i * SIZE + i; }
uint8_t urdl_index(uint8_t x, uint8_t y, uint8_t i) {
  return i * SIZE + (MAX_INDEX - i);
}
uint8_t (*index_functions[4])(uint8_t, uint8_t, uint8_t) = {
    x_index, y_index, uldr_index, urdl_index};

// rcdd
// urdl last
extern int8_t set_cell(uint8_t *board, uint8_t x, uint8_t y, uint8_t value,
                       bool *scores, bool *cell_selector) {
  if (y * SIZE + x >= AREA) {
    return -1;
  }
  if (board[y * SIZE + x] != 0 && board[y * SIZE + x] != value) {
    return -2;
  }

  for (int i = 0; i < SCRORE_SIZE; i++) {
    cell_selector[i] = false;
  }

  if (board[y * SIZE + x] != 0) {
    board[y * SIZE + x] = value | 128;
  } else {
    board[y * SIZE + x] = value;
  }

  cell_selector[x] = check(x, y, board, x_index);
  scores[x] = scores[0];
  cell_selector[5 + y] = check(x, y, board, y_index);
  scores[y + 5] = cell_selector[1];
  if (x == y && check(x, y, board, uldr_index)) {
    cell_selector[AREA] = true;
    scores[AREA] = true;
  }
  if (x == MAX_INDEX - y && check(x, y, board, urdl_index)) {
    cell_selector[AREA + 1] = true;
    scores[AREA + 1] = true;
  }

  return 0;
}

void sort_values(uint8_t *values, uint8_t size) {
  bool swapped = true;
  while (swapped) {
    swapped = false;
    for (int i = 0; i < size; i++) {
      if (values[i] > values[i + 1]) {
        uint8_t temp = values[i];
        values[i] = values[i + 1];
        values[i + 1] = temp;
        swapped = true;
      }
    }
  }
}

bool is_street(uint8_t *values) {
  uint8_t sorted_values[5];
  for (int i = 0; i < SIZE; i++) {
    sorted_values[i] = values[i] & 0b1111;
  }
  sort_values(sorted_values, SIZE);
  bool street = true;
  for (int i = 0; i < SIZE - 1; i++) {
    if (sorted_values[i] + 1 != sorted_values[i + 1]) {
      return false;
    }
  }
  return true;
}

int8_t min(int8_t a, int8_t b) { return a < b ? a : b; }

extern uint8_t get_fields_for_cell_selection(uint8_t cell_selection, uint8_t x,
                                             uint8_t y, uint8_t *fields,
                                             uint8_t *board,
                                             bool *field_selectors) {
  for (int i = 0; i < AREA; i++) {
    field_selectors[i] = false;
  }
  uint8_t values[SIZE];
  uint8_t indexes[SIZE];
  uint8_t free_fields = 0;
  for (int i = 0; i < SIZE; i++) {
    uint8_t index;
    if (cell_selection == AREA + 1) {
      index = 3;
    } else {
      index = cell_selection / SIZE;
    }
    indexes[i] = index_functions[index](x, y, i);
    values[i] = board[indexes[i]];
    if (values[i] < 128) {
      field_selectors[indexes[i]] = true;
      free_fields++;
    }
  }

  uint8_t card_count[13];
  for (int i = 0; i < 13; i++) {
    card_count[i] = 0;
  }

  for (int i = 0; i < SIZE; i++) {
    card_count[values[i] & 0b1111]++;
  }

  sort_values(card_count, 13);

  if (card_count[12] == 5) {
    return min(3, free_fields);
  } else if (card_count[12] == 4) {
    return min(2, free_fields);
  } else if (card_count[12] == 3) {
    if (card_count[11] == 2) {
      return min(2, free_fields);
    }
    return min(1, free_fields);
  } else if (card_count[12] == 2 && card_count[11] == 2) {
    return min(1, free_fields);
  } else if (is_street(values)) {
    return min(3, free_fields);
  }
  return 0;
}

extern bool finished(uint8_t *board) {
  for (int i = 0; i < AREA; i++) {
    if (board[i] == 0) {
      return false;
    }
  }
  return true;
}

extern uint8_t count_points(uint8_t *board, bool *scores) {
  uint8_t points = 0;
  for (int i = 0; i < AREA; i++) {
    if (board[i] >= 128) {
      points++;
    }
  }

  for (int i = 0; i < SCRORE_SIZE; i++) {
    if (scores[i]) {
      if (i < SIZE) {
        points += SIZE * 2 - 1 - i;
      } else if (i >= SIZE * 2) {
        points += 10;
      } else {
        points += SIZE * 3 - 1 - i;
      }
    }
  }
  return points;
}
