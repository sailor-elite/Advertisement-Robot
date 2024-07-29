//libraries not included in this program ;;;
#include "Audio.h"
#include "SD.h"
#include "FS.h"
#include "cstdlib"

// aaaaa
//bbbbb

// Digital I/O used
#define SD_CS 10
#define SPI_MOSI 13
#define SPI_MISO 11
#define SPI_SCK 12
#define I2S_DOUT 37
#define I2S_BCLK 38
#define I2S_LRC 39
#define InterruptPin 2


//aaaa
//aaaaaaa
// Parameters
#define Volume 17 // default 0...21
#define Baud 9600
#define MinMusicNumber 0 // It should be always 0
#define MaxMusicNumber 22
#define MinInterruptMusicNumber 0
#define MaxInterruptMusicNumber 5
#define TimerWakeup 30000000// wakeup 10 sec time
Audio audio;

const char *songs_list[] = {"/01.mp3", "/02.mp3", "/03.mp3", "/04.mp3", "/05.mp3", "/06.mp3", "/07.mp3", "/08.mp3", "/09.mp3", "/10.mp3",
                            "/11.mp3", "/12.mp3", "/13.mp3", "/14.mp3", "/15.mp3", "/16.mp3", "/17.mp3", "/18.mp3", "/19.mp3", "/20.mp3",
                            "/21.mp3", "/22.mp3"};

const char *interrupt_songs_list[] = {"/a4.mp3", "/a5.mp3", "/a6.mp3", "/a7.mp3", "/a8.mp3"};

int last_music_number = -1;
int last_interrupt_music_number = -1;
bool initial_song_played = false;
bool playing_interruption = false;
bool Request;


void IRAM_ATTR ISR()
{
    Request = true;
}

void setup()
{
    pinMode(SD_CS, OUTPUT);
    digitalWrite(SD_CS, HIGH);
    SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI);
    Serial.begin(Baud);
    if (!SD.begin(SD_CS))
    {
        Serial.println("Error accessing microSD card!");
        while (true)
            ;
    }
    audio.setPinout(I2S_BCLK, I2S_LRC, I2S_DOUT);
    audio.setVolume(Volume); // default 0...21

    audio.connecttoFS(SD, "/a2.mp3"); // Play the initial song

    pinMode(InterruptPin, INPUT_PULLUP);
    attachInterrupt(InterruptPin, ISR, RISING);
    Serial.print("koniec setup: ");
}

void number_generation()
{
    int music_number = -1;
    do
    {
        music_number = random(MinMusicNumber, MaxInterruptMusicNumber);
    } while (music_number == last_music_number);

    last_music_number = music_number;
    Serial.print("Music number: ");
    Serial.print(music_number);
    Serial.print(" Odtwarzam audio_file: ");
    Serial.println(songs_list[music_number]);

    audio.connecttoFS(SD, songs_list[music_number]);
}

void enterLightSleep()
{
    esp_sleep_enable_timer_wakeup(TimerWakeup);      
    esp_sleep_enable_ext0_wakeup(GPIO_NUM_2, 1); // Wake up on high level
    Serial.println("Entering light sleep");
    Serial.flush();
    esp_light_sleep_start();
    Serial.println("Woke up from light sleep");
}

void interrupt_number_generation()
{
    int interrupt_music_number = -1;
    do
    {
        interrupt_music_number = random(MinInterruptMusicNumber, MaxInterruptMusicNumber);
    } while (interrupt_music_number == last_interrupt_music_number);

    last_interrupt_music_number = interrupt_music_number;
    Serial.print("Music number: ");
    Serial.print(interrupt_music_number);
    Serial.print(" Odtwarzam audio_file: ");
    Serial.println(interrupt_songs_list[interrupt_music_number]);

    audio.connecttoFS(SD, interrupt_songs_list[interrupt_music_number]);
}

void loop()
{
    
    esp_sleep_wakeup_cause_t wakeup_reason;

    wakeup_reason = esp_sleep_get_wakeup_cause();

    if (wakeup_reason == ESP_SLEEP_WAKEUP_TIMER)
    {
        if (!audio.isRunning())
        {
            if (!initial_song_played)
            {
                initial_song_played = true; // Mark that the initial song has been played
                number_generation();        // Start playing the next song
            }
            else
            {
                number_generation(); // Continue playing random songs
            }
        }
        wakeup_reason = ESP_SLEEP_WAKEUP_UNDEFINED;
    }
    if (Request)
    {
        if (!audio.isRunning())
        {
            interrupt_number_generation(); // Play the interrupt random songs
        }
        Request = false;
    }
    audio.loop();
    if (!audio.isRunning())
    {
        enterLightSleep();
    }
}






