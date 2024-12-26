#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#define SIZE 5

extern uint8_t *init_board() {
  uint8_t *board = malloc(SIZE * SIZE);
  for (int i = 0; i < SIZE * SIZE; i++) {
    board[i] = 0;
  }
  return board;
}
// rrrrrcccccdd
// uldr first
extern bool *init_scores() {
  bool *scores = malloc(SIZE * 2 + 2);
  for (int i = 0; i < SIZE * 2 + 2; i++) {
    scores[i] = 0;
  }
  return scores;
}

extern int8_t set_cell(uint8_t *board, uint8_t x, uint8_t y, uint8_t value) {
  if (y * SIZE + x >= SIZE * SIZE) {
    return -1;
  }
  if (board[y * SIZE + x] != 0 && board[y * SIZE + x] != value) {
    return -2;
  }
  if (board[y * SIZE + x] != 0) {
    board[y * SIZE + x] = value | 128;
  } else {
    board[y * SIZE + x] = value;
  }
  return 0;
}

// ddcccccrrrrr
// uldr last
extern uint16_t update_score(uint8_t *board, uint8_t x, uint8_t y,
                             bool *scores) {
  uint16_t ret = 0;
  bool full = true;
  for (int i = 0; i < SIZE; i++) {
    if (board[x * SIZE + i] < 128) {
      full = false;
      break;
    }
  }
  if (full) {
    scores[x] = true;
    ret |= 1 << x;
  }

  full = true;
  for (int i = 0; i < SIZE; i++) {
    if (board[i * SIZE + y] < 128) {
      full = false;
      break;
    }
  }
  if (full) {
    scores[y] = true;
    ret |= 1 << (y + 5);
  }

  if (x == y) {
    full = true;
    for (int i = 0; i < SIZE; i++) {
      if (board[i * SIZE + i] < 128) {
        full = false;
        break;
      }
    }
    if (full) {
      scores[y] = true;
      ret |= 1 << 10;
    }
  }

  if (x == SIZE - 1 - y) {
    full = true;
    for (int i = 0; i < SIZE; i++) {
      if (board[i * SIZE + (SIZE - 1 - i)] < 128) {
        full = false;
        break;
      }
    }
    if (full) {
      scores[y] = true;
      ret |= 1 << 11;
    }
  }

  return ret;
}

extern bool finished(uint8_t *board) {
  for (int i = 0; i < SIZE * SIZE; i++) {
    if (board[i] == 0) {
      return false;
    }
  }
  return true;
}

extern uint8_t count_points(uint8_t *board, bool *scores) {
  uint8_t points = 0;
  for (int i = 0; i < SIZE * SIZE; i++) {
    if (board[i] >= 128) {
      points++;
    }
  }

  for (int i = 0; i < SIZE; i++) {
    if (scores[i]) {
      points += SIZE * 2 - 1 - i;
    }
  }

  for (int i = SIZE; i < SIZE * 2; i++) {
    if (scores[i]) {
      points += SIZE * 3 - 1 - i;
    }
  }

  for (int i = 10; i < 12; i++) {
    if (scores[i]) {
      points += 10;
    }
  }

  return points;
}
