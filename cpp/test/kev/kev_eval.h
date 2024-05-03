#ifndef KEV_EVAL_H
#define KEV_EVAL_H

#ifdef __cplusplus
extern "C" {
#endif

short kev_eval_5cards(int c1, int c2, int c3, int c4, int c5);
short kev_eval_6cards(int c1, int c2, int c3, int c4, int c5, int c6);
short kev_eval_7cards(int c1, int c2, int c3, int c4, int c5, int c6, int c7);
short kev_eval_8cards(int c1, int c2, int c3, int c4, int c5, int c6, int c7,
                      int c8);
short kev_eval_9cards(int c1, int c2, int c3, int c4, int c5, int c6, int c7,
                      int c8, int c9);

#ifdef __cplusplus
}  // closing brace for extern "C"
#endif

#endif
