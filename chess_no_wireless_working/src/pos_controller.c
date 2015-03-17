/*
 * pos_controller.c
 *
 * Created: 31.01.2014 23:54:58
 *  Author: student
 */ 

#include "asf.h"

#include "encoder.h"
#include "motor_shield.h"
#include "pos_controller.h"

#include "servo.h"

#include <math.h>



/* POINTS_PER_CM 59 */
/* CM_PER_SQUARE 2.625 */
#define CHESS_SQUARE_WIDTH 155 /* POINTS_PER_CM*CM_PER_SQUARE */


/* piece_(x/y) = {0,1,2,3,4,5,6,7} */
void controller_move_piece(int piece_x_start, int piece_y_start, int piece_x_end, int piece_y_end){
	
	/* We want to start on the center of the square */
	int center_offset = CHESS_SQUARE_WIDTH/2;
	
	/* Because the chess piece lags behind the magnet */
	int magnet_offset = CHESS_SQUARE_WIDTH/3;
	
	/* Move wagon under chess piece */
	controller_set_position(center_offset + piece_x_start*CHESS_SQUARE_WIDTH, MOTOR_1_X);
	controller_set_position(center_offset + piece_y_start*CHESS_SQUARE_WIDTH, MOTOR_2_Y);
	
	printf("x=%d, y=%d \n", encoder_read_x_pos(), encoder_read_y_pos());
	
	/* Move magnet into position */
	servo_magnet_set(1);
	delay_ms(400);
	
	/* Move chess piece */
	controller_set_position(center_offset + magnet_offset + piece_x_end*CHESS_SQUARE_WIDTH, MOTOR_1_X);
	controller_set_position(center_offset + magnet_offset + piece_y_end*CHESS_SQUARE_WIDTH, MOTOR_2_Y);	
	
	printf("x=%d, y=%d \n", encoder_read_x_pos(), encoder_read_y_pos());
	
	/* Remove magnet */
	servo_magnet_set(0);
	delay_ms(400);
	
	/* Reset position */
	
	controller_reset_position(MOTOR_1_X);
	controller_reset_position(MOTOR_2_Y);
	
}

void controller_move_wagon(int x_start, int y_start, int x_end, int y_end){
	
	controller_set_position(x_start, MOTOR_1_X);
	controller_set_position(y_start, MOTOR_2_Y);
	
	controller_set_position(x_end, MOTOR_1_X);
	controller_set_position(y_end, MOTOR_2_Y);
	
}

void controller_reset_position(ms_motor_t motor){
	
	controller_set_position(5, motor);
	ms_set_dir(0, motor); //towards origo
	
	//when in origo, drive the motor towards the stop
	ms_set_duty_cycle(20, motor);
	delay_ms(500);
	ms_set_duty_cycle(0, motor);
	
	switch (motor)
	{
		case MOTOR_1_X:
		encoder_reset_pos_x();
		break;
		
		case MOTOR_2_Y:
		encoder_reset_pos_y();
		break;
	}	
	
}


void controller_set_position(int pos, ms_motor_t axis){
	
	int current_pos, dir, speed;
	
	switch (axis)
	{
		case MOTOR_1_X:
		current_pos = encoder_read_x_pos();
		break;
		
		case MOTOR_2_Y:
		current_pos = encoder_read_y_pos();
		break;
	}
	
	
	dir = pos > current_pos ? 1 : 0; //if pos > current_pos, dir = 1;	
	speed = 40;

	
	ms_set_duty_cycle(speed, axis);
	
	while(abs(pos-current_pos)>5){
		
		switch (axis)
		{
			case MOTOR_1_X:
			current_pos = encoder_read_x_pos();
			break;
			
			case MOTOR_2_Y:
			current_pos = encoder_read_y_pos();
			break;
		}
	
		
		dir = pos > current_pos ? 1 : 0; //if pos > current_pos, dir = 1;
		
		ms_set_dir(dir, axis);
		
		
	}
	
	
	ms_set_duty_cycle(0, axis);
	
	
}