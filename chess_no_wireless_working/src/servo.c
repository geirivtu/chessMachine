/*
 * servo.c
 *
 * Created: 01.02.2014 16:58:37
 *  Author: student
 */ 

#include "asf.h"

#include "servo.h"

#define TC             TC0
#define TC_CHANNEL_WAVEFORM 0

#define SERVO_MAGNET 0
#define SERVO_SLAPPER 1

void servo_init(void){
	
	/* PWM initialize */
	
	/* Configure PIO Pins for TC */
	ioport_set_pin_mode(PIN_PA08B_TC0_A0, MUX_PA08B_TC0_A0); //M34_EN_PIN ( EXT2 7 ) ra
	//ioport_set_pin_mode(PIN_PC05D_TC1_B2, MUX_PC05D_TC1_B2); //M12_EN_PIN ( EXT2 8 ) rb
	
	/* Disable IO to enable peripheral mode) */
	ioport_disable_pin(PIN_PA08B_TC0_A0);
	//ioport_disable_pin(PIN_PC05D_TC1_B2);
	

	uint32_t ra, rb, rc;

	/* Configure the PMC to enable the TC module. */
	sysclk_enable_peripheral_clock(TC0);

	/* Init TC to waveform mode. */
	tc_init(TC, TC_CHANNEL_WAVEFORM,
	/* Waveform Clock Selection */
	TC_CMR_TCCLKS_TIMER_CLOCK3
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

	
	tc_write_rc(TC, TC_CHANNEL_WAVEFORM, rc);
	

	tc_write_ra(TC, TC_CHANNEL_WAVEFORM, ra);
	//tc_write_rb(TC, TC_CHANNEL_WAVEFORM, rb);

	/* Enable TC TC_CHANNEL_WAVEFORM. */
	tc_start(TC, TC_CHANNEL_WAVEFORM);
	
	/* PWM End */
		
	servo_magnet_set(0);
}

void servo_set_duty_cycle(int pwm_dc, int servo){
	
	if(pwm_dc >= 100) pwm_dc = 99;
	else if(pwm_dc<0) pwm_dc = 0;
	
	switch (servo)
	{
		case SERVO_MAGNET:
		tc_write_ra(TC, TC_CHANNEL_WAVEFORM, ((int)((100-pwm_dc)*tc_read_rc(TC, TC_CHANNEL_WAVEFORM)) /100.0));
		
		break;
		
		case SERVO_SLAPPER:
		tc_write_rb(TC, TC_CHANNEL_WAVEFORM, ((int)((100-pwm_dc)*tc_read_rc(TC, TC_CHANNEL_WAVEFORM))/100.0));
		
		break;
	}
	
}

void servo_magnet_set(int status){

		if(status){
			servo_set_duty_cycle(5, SERVO_MAGNET); /* magnet up */
		}else{
			servo_set_duty_cycle(8, SERVO_MAGNET); /* magnet down */
		}
}



