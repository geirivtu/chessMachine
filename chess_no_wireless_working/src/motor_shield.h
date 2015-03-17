/*
 * motor_shield.h
 *
 * Created: 31.01.2014 16:26:43
 *  Author: student
 */ 


#ifndef MOTOR_SHIELD_H_
#define MOTOR_SHIELD_H_

typedef enum { MOTOR_1_X, MOTOR_2_Y} ms_motor_t;


void ms_init();

void ms_run(ms_motor_t motor_nr);

void ms_stop(ms_motor_t motor_nr);

void ms_set_dir(int dir, ms_motor_t motor_nr);
	
void ms_set_duty_cycle(int pwm_dc, ms_motor_t motor_nr);	




#endif /* MOTOR_SHIELD_H_ */