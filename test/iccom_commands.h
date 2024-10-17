/*
 * This header file is shared between Linux and G4 and it includes all the
 * known iccom commands and replies
 */

#ifndef __ICCOM_COMMANDS_H__
#define __ICCOM_COMMANDS_H__

/*
 * CC-RH has different types compared to Linux, but since this file is shared
 * it should compile on both systems
 */
#ifdef LINUX_TEST_APP
	#include <stdint.h>
// #else
// 	typedef uint8	uint8_t;
// 	typedef uint16	uint16_t;
#endif

enum iccom_command {
	NONE = 0,
	ECHO,
	OS,
	BENCH,
};

// this is the common header shared between all commands
#define CMD_HEADER		\
		uint8_t cmd_id;

#define MAX_ECHO_DATA_SIZE		(4096U)

// #pragma pack(1)
struct echo_command {
	CMD_HEADER
	uint8_t data[MAX_ECHO_DATA_SIZE];
};


#endif //__ICCOM_COMMANDS_H__
