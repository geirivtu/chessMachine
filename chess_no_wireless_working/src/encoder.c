/*
 * encoder.c
 *
 * Created: 31.01.2014 13:45:19
 *  Author: student
 */ 



#include "encoder.h"

#include "asf.h"


/* EXT2 */
#define X_AXIS_OUT_2_PIN PIN_PC08 //EXT2 5
#define X_AXIS_OUT_1_PIN PIN_PB10 //EXT2 6

/* EXT2 */
#define Y_AXIS_OUT_2_PIN PIN_PA07 //EXT2 3
#define Y_AXIS_OUT_1_PIN PIN_PB02 //EXT2 4


int X_axis_pos = 0;
int Y_axis_pos = 0;


/* Callback funtion for x-axis interrupt pins */
static void x_axis_callback(void)
{
	int sensor1 = 0; int sensor2 = 0;
	static int sensor1_prev_value = 0;
	
	sensor1 = ioport_get_pin_level(X_AXIS_OUT_1_PIN);
	sensor2 = ioport_get_pin_level(X_AXIS_OUT_2_PIN);
	
	if ((sensor1_prev_value == LOW) && (sensor1 == HIGH)) {
		if (sensor2 == LOW) {
			X_axis_pos--;
			} else {
			X_axis_pos++;
		}
	}

	sensor1_prev_value = sensor1;
	
	//printf("%d, %d \n\t", sensor1, sensor2);
}

/* Callback funtion for x-axis interrupt pins */
static void y_axis_callback(void)
{
	int sensor1 = 0; int sensor2 = 0;
	static int sensor1_prev_value = 0;
	
	sensor1 = ioport_get_pin_level(Y_AXIS_OUT_1_PIN);
	sensor2 = ioport_get_pin_level(Y_AXIS_OUT_2_PIN);
	
	if ((sensor1_prev_value == LOW) && (sensor1 == HIGH)) {
		if (sensor2 == LOW) {
			Y_axis_pos--;
			} else {
			Y_axis_pos++;
		}
	}

	sensor1_prev_value = sensor1;
	
	//printf("%d, %d \n\t", sensor1, sensor2);
}


int encoder_read_x_pos(void){
	return X_axis_pos;
}


int encoder_read_y_pos(void){
	return Y_axis_pos;
}

void encoder_reset_pos_x(){
	X_axis_pos = 0;
}
void encoder_reset_pos_y(){
	Y_axis_pos = 0;
}


void encoder_init_gpio(void){
	
	/* Configure sensor out 1 pin to trigger an interrupt on falling edge */
	
	ioport_set_pin_dir(X_AXIS_OUT_1_PIN, IOPORT_DIR_INPUT);
	
	ioport_set_pin_mode(X_AXIS_OUT_1_PIN, IOPORT_MODE_PULLUP |
	IOPORT_MODE_GLITCH_FILTER);
	
	ioport_set_pin_sense_mode(X_AXIS_OUT_1_PIN, IOPORT_SENSE_BOTHEDGES);
	
	if (!gpio_set_pin_callback(X_AXIS_OUT_1_PIN, x_axis_callback, 1)) {
		printf("Set pin callback failure!\r\n");
		while (1) {
		}
	}
	gpio_enable_pin_interrupt(X_AXIS_OUT_1_PIN);
	
	
	/* Configure sensor out 2 pin to trigger an interrupt on falling edge */
	
	ioport_set_pin_dir(X_AXIS_OUT_2_PIN, IOPORT_DIR_INPUT);
	
	ioport_set_pin_mode(X_AXIS_OUT_2_PIN, IOPORT_MODE_PULLUP |
	IOPORT_MODE_GLITCH_FILTER);
	
	ioport_set_pin_sense_mode(X_AXIS_OUT_2_PIN, IOPORT_SENSE_BOTHEDGES);
	
	if (!gpio_set_pin_callback(X_AXIS_OUT_2_PIN, x_axis_callback, 1)) {
		printf("Set pin callback failure!\r\n");
		while (1) {
		}
	}
	gpio_enable_pin_interrupt(X_AXIS_OUT_2_PIN);
	
	
	
	
	/*******************************************/
	
	
	/* Configure sensor out 1 pin to trigger an interrupt on falling edge */
	
	ioport_set_pin_dir(Y_AXIS_OUT_1_PIN, IOPORT_DIR_INPUT);
	
	ioport_set_pin_mode(Y_AXIS_OUT_1_PIN, IOPORT_MODE_PULLUP |
	IOPORT_MODE_GLITCH_FILTER);
	
	ioport_set_pin_sense_mode(Y_AXIS_OUT_1_PIN, IOPORT_SENSE_BOTHEDGES);
	
	if (!gpio_set_pin_callback(Y_AXIS_OUT_1_PIN, y_axis_callback, 1)) {
		printf("Set pin callback failure!\r\n");
		while (1) {
		}
	}
	gpio_enable_pin_interrupt(Y_AXIS_OUT_1_PIN);
	
	
	/* Configure sensor out 2 pin to trigger an interrupt on falling edge */
	
	ioport_set_pin_dir(Y_AXIS_OUT_2_PIN, IOPORT_DIR_INPUT);
	
	ioport_set_pin_mode(Y_AXIS_OUT_2_PIN, IOPORT_MODE_PULLUP |
	IOPORT_MODE_GLITCH_FILTER);
	
	ioport_set_pin_sense_mode(Y_AXIS_OUT_2_PIN, IOPORT_SENSE_BOTHEDGES);
	
	if (!gpio_set_pin_callback(Y_AXIS_OUT_2_PIN, y_axis_callback, 1)) {
		printf("Set pin callback failure!\r\n");
		while (1) {
		}
	}
	gpio_enable_pin_interrupt(Y_AXIS_OUT_2_PIN);
	
}