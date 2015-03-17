/*
 * motor_shield.c
 *
 * Created: 31.01.2014 16:26:19
 *  Author: student
 */ 

#include "asf.h"

#include "motor_shield.h"

/* All pin on ext 2 header */
//#define M12_EN_PIN  PIN_PC27// Ext2 14
#define M1A_PIN		PIN_PA22 // Ext2 16
#define M2A_PIN		PIN_PC30 // // Ext2 18

//#define M34_EN_PIN	PIN_PC26// Ext2 13
#define M3A_PIN		PIN_PB11// Ext2 15
#define M4A_PIN		PIN_PA21 // Ext2 17

#define TC             TC1
#define TC_CHANNEL_WAVEFORM  2


void ms_set_duty_cycle(int pwm_dc, ms_motor_t motor_nr){
	
	if(pwm_dc >= 100) pwm_dc = 99;
	else if(pwm_dc<0) pwm_dc = 0;
	
	switch (motor_nr)
	{
		case MOTOR_1_X:
			tc_write_rb(TC, TC_CHANNEL_WAVEFORM, ((int)((100-pwm_dc)*tc_read_rc(TC, TC_CHANNEL_WAVEFORM))/100.0));
		break;
		
		case MOTOR_2_Y:
			tc_write_ra(TC, TC_CHANNEL_WAVEFORM, ((int)((100-pwm_dc)*tc_read_rc(TC, TC_CHANNEL_WAVEFORM)) /100.0));
			
		break;
	}
	
}

void ms_init(){

	/* PWM initialize */ 
	
	/* Configure PIO Pins for TC */
	ioport_set_pin_mode(PIN_PC04D_TC1_A2, MUX_PC04D_TC1_A2); //M34_EN_PIN ( EXT2 7 ) ra
	ioport_set_pin_mode(PIN_PC05D_TC1_B2, MUX_PC05D_TC1_B2); //M12_EN_PIN ( EXT2 8 ) rb
	
	/* Disable IO to enable peripheral mode) */
	ioport_disable_pin(PIN_PC04D_TC1_A2);
	ioport_disable_pin(PIN_PC05D_TC1_B2);
	

	uint32_t ra, rb, rc;

	/* Configure the PMC to enable the TC module. */
	sysclk_enable_peripheral_clock(TC1);

	/* Init TC to waveform mode. */
	tc_init(TC, TC_CHANNEL_WAVEFORM,
			/* Waveform Clock Selection */
			TC_CMR_TCCLKS_TIMER_CLOCK2
			| TC_CMR_WAVE /* Waveform mode is enabled */
			
			| TC_CMR_ACPA_SET /* RA Compare Effect: set */
			| TC_CMR_ACPC_CLEAR /* RC Compare Effect: clear */
			
			 
			| TC_CMR_EEVT_XC0_OUTPUT /* TIOB Direction output */
			
			| TC_CMR_BCPB_SET /* RB Compare Effect: set */
			| TC_CMR_BCPC_CLEAR /* RC Compare Effect: clear */
			
			
			| TC_CMR_CPCTRG /* UP mode with automatic trigger on RC Compare */
	);

	/*  PBA = 6 MHz, DIV = 8, freq = 500 Hz, rc = PBA/DIV/freq */
	rc = 30000;
	ra = rc;
	rb = rc;
			
	tc_write_rc(TC, TC_CHANNEL_WAVEFORM, rc);
	

	tc_write_ra(TC, TC_CHANNEL_WAVEFORM, ra);
	tc_write_rb(TC, TC_CHANNEL_WAVEFORM, rb);

	/* Enable TC TC_CHANNEL_WAVEFORM. */
	tc_start(TC, TC_CHANNEL_WAVEFORM);
	
	/* PWM End */
	
	/* Motor 1 pins */
	//ioport_set_pin_dir(M12_EN_PIN, IOPORT_DIR_OUTPUT);
	//ioport_set_pin_level(M12_EN_PIN, IOPORT_PIN_LEVEL_LOW);
	
	ioport_set_pin_dir(M1A_PIN, IOPORT_DIR_OUTPUT);
	ioport_set_pin_level(M1A_PIN, IOPORT_PIN_LEVEL_LOW);
	
	ioport_set_pin_dir(M2A_PIN, IOPORT_DIR_OUTPUT);
	ioport_set_pin_level(M2A_PIN, IOPORT_PIN_LEVEL_LOW);
	
	/* Motor 2 pins */
	//ioport_set_pin_dir(M34_EN_PIN, IOPORT_DIR_OUTPUT);
	//ioport_set_pin_level(M34_EN_PIN, IOPORT_PIN_LEVEL_LOW);
	
	ioport_set_pin_dir(M3A_PIN, IOPORT_DIR_OUTPUT);
	ioport_set_pin_level(M3A_PIN, IOPORT_PIN_LEVEL_LOW);
	
	ioport_set_pin_dir(M4A_PIN, IOPORT_DIR_OUTPUT);
	ioport_set_pin_level(M4A_PIN, IOPORT_PIN_LEVEL_LOW);
	
}

void ms_run(ms_motor_t motor_nr){
	
	switch (motor_nr)
	{
		case MOTOR_1_X:
		
		//ioport_set_pin_level(M12_EN_PIN, HIGH);
			
		break;
		
		case MOTOR_2_Y:
		
		
		break;
	}
	
}


void ms_stop(ms_motor_t motor_nr){
	
	ms_set_duty_cycle(0, motor_nr);
	
}

/* dir = {0, 1} */
void ms_set_dir(int dir, ms_motor_t motor_nr){
	
	switch (motor_nr)
	{
		case MOTOR_1_X:
			ioport_set_pin_level(M1A_PIN, dir);
			ioport_set_pin_level(M2A_PIN, !dir);
		break;
		
		case MOTOR_2_Y:
			ioport_set_pin_level(M3A_PIN, dir);
			ioport_set_pin_level(M4A_PIN, !dir);		
		break;
	}

	
}


