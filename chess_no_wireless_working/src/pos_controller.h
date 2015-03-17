/*
 * pos_controller.h
 *
 * Created: 31.01.2014 23:55:26
 *  Author: student
 */ 


#ifndef POS_CONTROLLER_H_
#define POS_CONTROLLER_H_


void controller_move_wagon(int x_start, int y_start, int x_end, int y_end);
void controller_reset_position(ms_motor_t motor);
void controller_set_position(int pos, ms_motor_t axis);
void controller_move_piece(int piece_x_start, int piece_y_start, int piece_x_end, int piece_y_end);

#endif /* POS_CONTROLLER_H_ */