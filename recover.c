#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //Checki if argument count is 2
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    //Open file for reading
    FILE *input_file = fopen(argv[1], "r");

    //check that the input_file is valid
    if(input_file == NULL)
    {
        printf("Could not open file");
        return 2;
    }


    //store blocks pf 512 bytes in an array
    unsigned char buffer[512];

    //number of images counted
    int count_image = 0;

    //filepointer for recovered images
    FILE *output_file = NULL;

    //char filename[8]
    char *filename = malloc(8 * sizeof(char));

    //read blocks of 512 Bytes
    while (fread(buffer, sizeof(char), 512, input_file))
    {
        //check if bytes indicate start of JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //write the JPEG filenames
            sprintf(filename, "%03i.jpg", count_image);

            //Open ouput_file for writing
            output_file = fopen(filename, "w");

            //Count number of images found
            count_image++;
        }
            //check if ouput has been used for valid input
            if (output_file != NULL)
            {
                fwrite(buffer, sizeof(char), 512, output_file);
            }
    }
    free(filename);
    fclose(output_file);
    fclose(input_file);

    return 0;
}