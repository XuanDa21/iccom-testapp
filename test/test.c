#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <time.h>
#include "iccom.h"
#include "iccom_commands.h"

#define NS_IN_MS (1000 * 1000)
#define MS_IN_S 1000
#define NS_IN_S (NS_IN_MS * MS_IN_S)

// Function prototypes
void print_help(int argc, char **argv);
int parse_input_args(int argc, char **argv);
int run_iccom_test();

// static variables
static int iteration_count_flag = 1;
static int size_flag = 1;
static uint8_t rbuf[ICCOM_BUF_MAX_SIZE];

// global variables
int ret, len, channel_no;
Iccom_channel_t pch;
Iccom_init_param ip;
Iccom_send_param sp;

void print_help(int argc, char **argv)
{
    printf("Usage: %s [-s|-c|-n|-h]\n", argv[0]);
    printf("    -n: number of iterations to test\n");
    printf("    -s: size of each iteration\n");
    printf("    -c: select channel for test (0-7)\n");
    printf("    -h: show this help\n");
}

int parse_input_args(int argc, char **argv)
{
    int c;

    while ((c = getopt(argc, argv, "n:s:c:h")) != -1)
    {
        switch (c)
        {
            case 'n':
                iteration_count_flag = strtoul(optarg, NULL, 10);
                break;
            case 's':
                size_flag = strtoul(optarg, NULL, 10);
                break;
            case 'c':
                channel_no = strtoul(optarg, NULL, 10);
                break;
            case 'h':
            case '?':
                print_help(argc, argv);
                return -1;
        }
    }
    

    if (iteration_count_flag < 1)
    {
        printf("Iteration count cannot (%d) be less than 1\n", iteration_count_flag);
        return -1;
    }

    if (channel_no > 7 || channel_no < 0)
    {
        printf("The channel for ICCOM testing must be within the range of 0 to 7 \n");
        return -1;
    }

    return 0;
}

static void callback(enum Iccom_channel_number ch, uint32_t sz, uint8_t *buf)
{
    printf("Received %u bytes: ", sz);
    printf("\n");
}

int run_iccom_test()
{
    struct echo_command cmd = {.cmd_id = NONE};
    struct timespec start_time, end_time;
    int curr_iter, ret = 0, err_cnt = 0;
    uint64_t elapsed_ms, transferred_data;
    ret = clock_gettime(CLOCK_MONOTONIC, &start_time);
    if (ret < 0)
    {
        printf("clock_gettime failed at start\n");
        return ret;
    }

    ip.recv_buf = rbuf;
    ip.channel_no = channel_no;
    ip.recv_cb = callback;
    ret = Iccom_lib_Init(&ip, &pch);
    if (ret == ICCOM_OK)
    {
        printf("ICCOM initialized successfully.\n");
    }

    for (curr_iter = 0; curr_iter < iteration_count_flag; curr_iter++)
    {
        if (size_flag == 0) {
            sp.send_buf = NULL;  
        } else {
            memset(cmd.data, (curr_iter & 0xFF), size_flag);  
            sp.send_buf = (uint8_t *)&cmd;  
        }
        size_t pkt_size = size_flag;
        do
        {
            sp.send_size = pkt_size;
            sp.channel_handle = pch;
            ret = Iccom_lib_Send(&sp);
            if (ret != ICCOM_OK)
            {
                printf("Iccom_lib_Send error %d\n", ret);
                return -1;
            }
        } while (ret < 0);
    }

    ret = clock_gettime(CLOCK_MONOTONIC, &end_time);
    if (ret < 0)
    {
        printf("clock_gettime failed at end\n");
        return ret;
    }

    elapsed_ms = (end_time.tv_sec - start_time.tv_sec) * MS_IN_S + (end_time.tv_nsec - start_time.tv_nsec) / NS_IN_MS;
    transferred_data = size_flag * iteration_count_flag;
    printf("Elapsed time [ms]: %lu\n", elapsed_ms);
    printf("Data transferred: %lu\n", transferred_data);
    printf("Throughput: %lu bytes/s\n", (transferred_data * 1000) / elapsed_ms);
    printf("Throughput: %1.2f MB/s\n", (transferred_data * 1000) / elapsed_ms / 1024.0 / 1024.0);
    printf("Error count: %d\n", err_cnt);
    return ret;
}


int main(int argc, char **argv)
{
    int ret = 0;
    ret = parse_input_args(argc, argv);
    if (ret)
    {
        return ret;
    }
    ret = run_iccom_test();
    return ret;
}