#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


void led()
{
	pinMode(13, OUTPUT);
	while(1)
	{
		digitalWrite(13, LOW);
	        delay(1000);
	        digitalWrite(13, HIGH);
	        delay(1000);
	}

}

int main(void)
{
	led();

	return 0;
}
