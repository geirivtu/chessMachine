/*
 * encoder.h
 *
 * Created: 31.01.2014 13:45:38
 *  Author: student
 */ 


#ifndef ENCODER_H_
#define ENCODER_H_

void encoder_init_gpio(void);

int encoder_read_x_pos(void);

int encoder_read_y_pos(void);

void encoder_reset_pos_x();

void encoder_reset_pos_y();

#endif /* ENCODER_H_ */