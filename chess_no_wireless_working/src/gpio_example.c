/**
 * \file
 *
 * \brief GPIO interrupt example.
 *
 * Copyright (c) 2012 - 2013 Atmel Corporation. All rights reserved.
 *
 * \asf_license_start
 *
 * \page License
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. The name of Atmel may not be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * 4. This software may only be redistributed and used in connection with an
 *    Atmel microcontroller product.
 *
 * THIS SOFTWARE IS PROVIDED BY ATMEL "AS IS" AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT ARE
 * EXPRESSLY AND SPECIFICALLY DISCLAIMED. IN NO EVENT SHALL ATMEL BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 * \asf_license_stop
 *
 */

/**
 * \mainpage
 * \section intro Introduction
 * This example shows how to configure GPIO module to trigger an interrupt
 * and an event.
 *
 * The push button 0 is configured to trigger a GPIO interrupt when it is
 * pressed. In the interrupt handler, the LED0 will be toggled every time.
 *
 * The \ref EXAMPLE_PIN_EVENT is configured to trigger a GPIO event when
 * detecting a falling edge. Each time a new event is coming, it will trigger
 * the PDCA to send a character to the USART without CPU usage.
 *
 * \section files Main Files
 * - gpio.c: GPIO driver implementation;
 * - gpio.h: GPIO driver header file;
 * - gpio_example.c: GPIO example application.
 *
 * \section compilinfo Compilation Information
 * This software is written for GNU GCC and IAR Embedded Workbench
 * for Atmel. Other compilers may or may not work.
 *
 * \section deviceinfo Device Information
 * SAM4L device can be used.
 *
 * \section configinfo Configuration Information
 * This example has been tested with the following configuration:
 * - SAM4L evaluation kit;
 * - SAM4L Xplained Pro;
 * - SAM4L8 Xplained Pro;
 * - PC terminal settings:
 *   - 115200 bps,
 *   - 8 data bits,
 *   - no parity bit,
 *   - 1 stop bit,
 *   - no flow control.
 *
 * \section contactinfo Contact Information
 * For further information, visit
 * <A href="http://www.atmel.com">Atmel</A>.\n
 * Support and FAQ: http://support.atmel.com/
 */
#include "asf.h"
#include "conf_example.h"

#include "encoder.h"
#include "motor_shield.h"
#include "pos_controller.h"
#include "servo.h"



/**
 * Configure serial console.
 */
static void configure_console(void)
{
	const usart_serial_options_t uart_serial_options = {
		.baudrate = CONF_UART_BAUDRATE,
#ifdef CONF_UART_CHAR_LENGTH
		.charlength = CONF_UART_CHAR_LENGTH,
#endif
		.paritytype = CONF_UART_PARITY,
#ifdef CONF_UART_STOP_BITS
		.stopbits = CONF_UART_STOP_BITS,
#endif
	};

	/* Configure console. */
	stdio_serial_init(CONF_UART, &uart_serial_options);
}



/**
 * Push button 0 interrupt callback.
 */
static void pb0_callback(void)
{
	/* Toggle LED when an interrupt happen on push button */
	LED_Toggle(LED0);	
	printf("x=%d, y=%d \n", encoder_read_x_pos(), encoder_read_y_pos());
	
	//static pwm_dc = 100;
	//ms_set_duty_cycle(pwm_dc, MOTOR_1_X);
	//pwm_dc -= 10;
	
	//ms_set_dir(1, MOTOR_1_X);
	
	static int magnet = 0;
	
	//servo_magnet_set(magnet);
	//magnet = !magnet;
	
	
}



/**
 * \brief Main entry point for GPIO example.
 */
int main(void)
{
	/* Initialize the SAM system */
	sysclk_init();
	board_init();

	/* Initialize the console uart */
	configure_console();

	/* Output example information */
	printf("\r\n\r\n-- GPIO interrupt and event example --\r\n");
	printf("-- %s\r\n", BOARD_NAME);
	printf("-- Compiled: %s %s --\r\n", __DATE__, __TIME__);

	/* Configure push button 0 to trigger an interrupt on falling edge */
	ioport_set_pin_dir(EXAMPLE_BUTTON_INT, IOPORT_DIR_INPUT);
	
	ioport_set_pin_mode(EXAMPLE_BUTTON_INT, IOPORT_MODE_PULLUP |
			IOPORT_MODE_GLITCH_FILTER);
			
	ioport_set_pin_sense_mode(EXAMPLE_BUTTON_INT, IOPORT_SENSE_FALLING);
	
	if (!gpio_set_pin_callback(EXAMPLE_BUTTON_INT, pb0_callback, 1)) {
		printf("Set pin callback failure!\r\n");
		while (1) {
		}
	}
	gpio_enable_pin_interrupt(EXAMPLE_BUTTON_INT);
	printf("Press %s to trigger LED.\r\n", BUTTON_0_NAME);
	
	
	delay_init(F_CPU);
	
	/* Initialize interrupt gpio */
    encoder_init_gpio();
	
	/* Initialize motor shield */
	ms_init();
	
	/* Initialize servos */
	servo_init();
	
	
	//ms_run(MOTOR_1_X);
	//ms_set_dir(1, MOTOR_1_X);
	
	//controller_set_position(200, MOTOR_2_Y);
	//controller_set_position(200, MOTOR_1_X);
	
	//servo_magnet_set(1);
	
	controller_move_piece(5,1,0,3);
	
	while (1) {
		
	}
}


