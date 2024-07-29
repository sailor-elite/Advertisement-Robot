#include "Arduino.h"
#include "WiFi.h"
#include "Audio.h"
#include "SD.h"
#include "FS.h"
#include "cstdlib"

// Digital I/O used
#define SD_CS          10
#define SPI_MOSI      13
#define SPI_MISO      11
#define SPI_SCK       12
#define I2S_DOUT      37
#define I2S_BCLK      38
#define I2S_LRC       39

Audio audio;

const char* songs_list[] = {"/01.mp3", "/02.mp3", "/03.mp3", "/04.mp3", "/05.mp3", "/06.mp3", "/07.mp3", "/08.mp3", "/09.mp3", "/10.mp3",
 "/11.mp3", "/12.mp3", "/13.mp3", "/14.mp3", "/15.mp3", "/16.mp3", "/17.mp3", "/18.mp3", "/19.mp3", "/20.mp3", "/21.mp3", "/22.mp3"};
int last_music_number = -1;
bool initial_song_played = false;

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
    if (!audio.isRunning()) {
        if (!initial_song_played) {
            initial_song_played = true; // Mark that the initial song has been played
            number_generation(); // Start playing the next song
        } else {
            number_generation(); // Continue playing random songs
        }
    }
}