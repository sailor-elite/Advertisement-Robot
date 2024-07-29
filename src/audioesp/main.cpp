#include "Arduino.h"
#include "WiFi.h"
#include "Audio.h"
#include "SD.h"
#include "FS.h"
#include "cstdlib"

// Digital I/O used
#define SD_CS         10
#define SPI_MOSI      13
#define SPI_MISO      11
#define SPI_SCK       12
#define I2S_DOUT      37
#define I2S_BCLK      38
#define I2S_LRC       39
#define PIR            2

Audio audio;

const char* songs_list[] = {"/01.mp3", "/02.mp3", "/03.mp3", "/04.mp3", "/05.mp3", "/06.mp3", "/07.mp3", "/08.mp3", "/09.mp3", "/10.mp3",
 "/11.mp3", "/12.mp3", "/13.mp3", "/14.mp3", "/15.mp3", "/16.mp3", "/17.mp3", "/18.mp3", "/19.mp3", "/20.mp3", "/21.mp3", "/22.mp3"};
int last_music_number = -1;
bool initial_song_played = false;
bool playing_interruption = false;




volatile int interruptCounter;  //for counting interrupt
int totalInterruptCounter;   	//total interrupt counting
int LED_STATE=LOW;
hw_timer_t * timer = NULL;      //H/W timer defining (Pointer to the Structure)

portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;


void IRAM_ATTR onTimer() {      //Defining Inerrupt function with IRAM_ATTR for faster access
 portENTER_CRITICAL_ISR(&timerMux);
 interruptCounter++;
 portEXIT_CRITICAL_ISR(&timerMux);
}



void setup() {
    pinMode(SD_CS, OUTPUT);
    digitalWrite(SD_CS, HIGH);
    SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
    Serial.begin(115200);
    if (!SD.begin(SD_CS)) {
        Serial.println("Error accessing microSD card!");
        while (true);
    }
    audio.setPinout(I2S_BCLK, I2S_LRC, I2S_DOUT);
    audio.setVolume(17); // default 0...21

    audio.connecttoFS(SD, "/a2.mp3"); // Play the initial song

    timer = timerBegin(0, 80, true);           	// timer 0, prescalar: 80, UP counting
    timerAttachInterrupt(timer, &onTimer, true); 	// Attach interrupt
    timerAlarmWrite(timer, 100000, true);  		// Match value= 1000000 for 1 sec. delay.
    timerAlarmEnable(timer);           			// Enable Timer with interrupt (Alarm Enable)
}

void number_generation() {
    int music_number = -1; // Losowanie liczby od 1 do 22
    do {
        music_number = random(0, 22);
    } while (music_number == last_music_number);

    last_music_number = music_number;
    Serial.print("Music number: ");
    Serial.print(music_number);
    Serial.print(" Odtwarzam audio_file: ");
    Serial.println(songs_list[music_number]);

    audio.connecttoFS(SD, songs_list[music_number]);
}

void loop() {
    audio.loop();

 if (interruptCounter > 0) {
 
   portENTER_CRITICAL(&timerMux);
   interruptCounter--;
   portEXIT_CRITICAL(&timerMux);
 
   totalInterruptCounter++;         	//counting total interrupt

   if (!audio.isRunning() ) {
        if (!initial_song_played) {
            initial_song_played = true; // Mark that the initial song has been played
            number_generation(); // Start playing the next song
        } else {
            number_generation(); // Continue playing random songs
        }
    }

   Serial.print("An interrupt as occurred. Total number: ");
   Serial.println(totalInterruptCounter);
 }
 
}