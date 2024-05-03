extern short eval_5cards_fast(int c1, int c2, int c3, int c4, int c5);
extern short eval_6cards_fast(int c1, int c2, int c3, int c4, int c5, int c6);
extern short eval_7cards_fast(int c1, int c2, int c3, int c4, int c5, int c6,
                              int c7);
extern short eval_8cards_fast(int c1, int c2, int c3, int c4, int c5, int c6,
                              int c7, int c8);
extern short eval_9cards_fast(int c1, int c2, int c3, int c4, int c5, int c6,
                              int c7, int c8, int c9);

int deck[52] = {
    98306,     81922,     73730,     69634,     164099,    147715,    139523,
    135427,    295429,    279045,    270853,    266757,    557831,    541447,
    533255,    529159,    1082379,   1065995,   1057803,   1053707,   2131213,
    2114829,   2106637,   2102541,   4228625,   4212241,   4204049,   4199953,
    8423187,   8406803,   8398611,   8394515,   16812055,  16795671,  16787479,
    16783383,  33589533,  33573149,  33564957,  33560861,  67144223,  67127839,
    67119647,  67115551,  134253349, 134236965, 134228773, 134224677, 268471337,
    268454953, 268446761, 268442665,
};

short kev_eval_5cards(int c1, int c2, int c3, int c4, int c5) {
  return eval_5cards_fast(deck[c1], deck[c2], deck[c3], deck[c4], deck[c5]);
}

short kev_eval_6cards(int c1, int c2, int c3, int c4, int c5, int c6) {
  return eval_6cards_fast(deck[c1], deck[c2], deck[c3], deck[c4], deck[c5],
                          deck[c6]);
}

short kev_eval_7cards(int c1, int c2, int c3, int c4, int c5, int c6, int c7) {
  return eval_7cards_fast(deck[c1], deck[c2], deck[c3], deck[c4], deck[c5],
                          deck[c6], deck[c7]);
}

short kev_eval_8cards(int c1, int c2, int c3, int c4, int c5, int c6, int c7,
                      int c8) {
  return eval_8cards_fast(deck[c1], deck[c2], deck[c3], deck[c4], deck[c5],
                          deck[c6], deck[c7], deck[c8]);
}

short kev_eval_9cards(int c1, int c2, int c3, int c4, int c5, int c6, int c7,
                      int c8, int c9) {
  return eval_9cards_fast(deck[c1], deck[c2], deck[c3], deck[c4], deck[c5],
                          deck[c6], deck[c7], deck[c8], deck[c9]);
}
