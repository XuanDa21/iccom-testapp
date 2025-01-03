#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>
#include <time.h>
#include "iccom.h"

#define CMD_HEADER \
    uint8_t cmd_id;
#define MAX_ECHO_DATA_SIZE (8192U)
#define NS_IN_MS (1000 * 1000)
#define MS_IN_S 1000
#define NS_IN_S (NS_IN_MS * MS_IN_S)
#define DELAY_US 20000

// Function prototypes
void print_help(int argc, char **argv);
int parse_input_args(int argc, char **argv);
int run_iccom_test();

// static variables
static int iteration_count_flag = 1;
static int size_flag = 1;
static int buf_flag = 1;
static uint8_t rbuf[ICCOM_BUF_MAX_SIZE];

// global variables
int ret, len, channel_no, minutes = 0;
uint64_t rec_bytes = 0;
uint8_t *recv_buf;
enum iccom_command
{
    NONE = 0,
};

struct echo_command
{
    CMD_HEADER
    uint8_t data[MAX_ECHO_DATA_SIZE];
};

void print_help(int argc, char **argv)
{
    printf("Usage: %s [-s|-c|-n|-b|-m| -h]\n", argv[0]);
    printf("    -n: number of iterations to test\n");
    printf("    -s: size of each iteration\n");
    printf("    -c: select a channel for test (0-7)\n");
    printf("    -b: set the buffer, where 0 sets the value to NULL, and 1 means it is not NULL (optional)\n");
    printf("    -m: Set the duration for data transfer (in minutes)\n");
    printf("    -h: show this help\n");
}

int parse_input_args(int argc, char **argv)
{
    int c;

    while ((c = getopt(argc, argv, "n:s:c:b:m:h")) != -1)
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
        case 'b':
            buf_flag = strtoul(optarg, NULL, 10);
            break;
        case 'm':
            minutes = strtoul(optarg, NULL, 10);
            break;
        case 'h':
            print_help(argc, argv);
            return -1;
        }
    }

    if (iteration_count_flag < 1)
    {
        printf("Iteration count cannot (%d) be less than 1\n", iteration_count_flag);
        return -1;
    }
    if (minutes < 0)
    {
        printf("Duration in minutes cannot be less than 0\n");
        return -1;
    }
    return 0;
}

static void callback(enum Iccom_channel_number ch, uint32_t sz, uint8_t *buf)
{
    printf("[CA5x channel %d] Received %u bytes", ch, sz);
    printf("\n");
    if (minutes == 0) {
        if (recv_buf == NULL) {
            recv_buf = malloc(size_flag * iteration_count_flag);
            if (recv_buf == NULL) {
                printf("Failed to allocate memory for recv_buf\n");
                return; 
            }
        }
        // Copy the received data into recv_buf at the correct offset
        memcpy(recv_buf + rec_bytes, buf, sz);
        rec_bytes += sz;  
    } else {
        rec_bytes += sz; 
    }
}

int run_iccom_test()
{
    uint8_t *total_sent_buf = malloc(size_flag * iteration_count_flag);  // Allocate buffer for all sent data
    uint64_t sent_offset = 0;                                            // Keep track of the position in the sent buffer

    Iccom_channel_t pch;
    Iccom_init_param ip;
    Iccom_send_param sp;
    struct echo_command cmd = {.cmd_id = NONE};
    struct timespec start_time, current_time;
    int curr_iter, ret = 0;
    uint64_t elapsed_ms, transferred_bytes, total_duration_ms;

    // Calculate the total duration in milliseconds
    total_duration_ms = minutes * MS_IN_S * 60;
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
    if (ret != ICCOM_OK)
    {
        printf("Iccom_lib_Init error %d\n", ret);
        return 1;
    }

    if (minutes > 0)
    {
        int i = 0;
        while (1)
        {
            ret = clock_gettime(CLOCK_MONOTONIC, &current_time);
            if (ret < 0)
            {
                printf("clock_gettime failed during execution\n");
                return ret;
            }

            elapsed_ms = ((current_time.tv_sec - start_time.tv_sec) * MS_IN_S +
                          (current_time.tv_nsec - start_time.tv_nsec) / NS_IN_MS);

            if (elapsed_ms >= total_duration_ms)
            {
                printf("\nSpecified duration of %d minutes reached. Stopping the test.\n", minutes);
                break;
            }
            
            memset(cmd.data, i & 0xFF, size_flag);
            sp.send_buf = (uint8_t *)&cmd;
            sp.send_size = size_flag;
            sp.channel_handle = pch;

            ret = Iccom_lib_Send(&sp);
            if (ret != ICCOM_OK)
            {
                printf("Iccom_lib_Send error %d\n", ret);
                return 1;
            }
            printf("[CA5x channel %d] Sent %d bytes\n", channel_no, size_flag);
            usleep(DELAY_US);
            ++i;
        }

        // Compare sent and received data after the duration
        transferred_bytes = size_flag * i;
        if (rec_bytes == transferred_bytes)
        {
            printf("Data sent and received are equal. \n");
        }
        else
        {
            printf("Data mismatch between sent (%lu bytes) and received (%lu bytes).\n", transferred_bytes, rec_bytes);
            exit(0);
        }
        printf("Bytes transferred: %lu\n", transferred_bytes);
        printf("Bytes received: %lu\n", rec_bytes);
        printf("Elapsed time [ms]: %lu\n", elapsed_ms);
        printf("Throughput: %lu bytes/s\n", (transferred_bytes * 1000) / elapsed_ms);
        printf("Throughput: %1.2f MB/s\n", (transferred_bytes * 1000) / elapsed_ms / 1024.0 / 1024.0);
    }
    else
    {
        for (curr_iter = 0; curr_iter < iteration_count_flag; curr_iter++)
        {
            if (buf_flag == 0)
            {
                sp.send_buf = NULL;
            }
            else
            {
                memset(cmd.data, (curr_iter & 0xFF), size_flag);
                sp.send_buf = (uint8_t *)&cmd;
                sp.send_size = size_flag;
                sp.channel_handle = pch;
            }

            memcpy(total_sent_buf + sent_offset, sp.send_buf, sp.send_size);
            sent_offset += sp.send_size;

            ret = Iccom_lib_Send(&sp);
            if (ret != ICCOM_OK)
            {
                printf("Iccom_lib_Send error %d\n", ret);
                return 1;
            }
            printf("[CA5x channel %d] Sent %d bytes\n", channel_no, size_flag);
            usleep(DELAY_US);
        }
        
        if (rec_bytes == sent_offset && memcmp(total_sent_buf, recv_buf, sent_offset) == 0)  // Compare total buffers
        {
            printf("All data sent and received are equal.\n");
        }
        else
        {
            printf("Data mismatch between sent (%lu bytes) and received (%lu bytes).\n", sent_offset, rec_bytes);
            exit(0);
        }

        // Clean up
        free(total_sent_buf); 
        ret = clock_gettime(CLOCK_MONOTONIC, &current_time);
        if (ret < 0)
        {
            printf("clock_gettime failed at end\n");
            return ret;
        }

        elapsed_ms = ((current_time.tv_sec - start_time.tv_sec) * MS_IN_S +
                      (current_time.tv_nsec - start_time.tv_nsec) / NS_IN_MS);
        transferred_bytes = size_flag * iteration_count_flag;
        printf("Bytes transferred: %lu\n", transferred_bytes);
        printf("Bytes received: %lu\n", rec_bytes);
        printf("Elapsed time [ms]: %lu\n", elapsed_ms);
        printf("Throughput: %lu bytes/s\n", (transferred_bytes * 1000) / elapsed_ms);
        printf("Throughput: %1.2f MB/s\n", (transferred_bytes * 1000) / elapsed_ms / 1024.0 / 1024.0);
    }

    ret = Iccom_lib_Final(pch);
    if (ret != ICCOM_OK)
    {
        printf("Iccom_lib_Final error %d\n", ret);
        return 1;
    }

    return ret;
}

int main(int argc, char **argv)
{
    int ret = 0;
    ret = parse_input_args(argc, argv);
    if (ret < 0)
    {
        return 1;
    }

    ret = run_iccom_test();
    if (ret < 0)
    {
        return 1;
    }

    return 0;
}
