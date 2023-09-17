#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]){
    // Mirror the arguments like so
    // cobalt -e "import('rpyc').cli(ARG1, ARG2, ARG3, ...)"

    // use popen to run the command

    char command[256] = "cobalt -e \"import('rpyc').cli("; // 256 is arbitrary
    for(int i = 1; i < argc; i++){
        strcat(command, argv[i]);
        if(i != argc - 1){
            strcat(command, ", ");
        }
    }
    strcat(command, ")\"");
    
    FILE *fp = popen(command, "r");
    char buff[256];
    while(fgets(buff, 256, fp) != NULL){
        printf("%s", buff);
    }
    pclose(fp);
    return 0;
}