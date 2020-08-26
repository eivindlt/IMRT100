#include "DualVNH5019MotorShield.h"
#include "NewPing.h"



#define V_MAX 500
#define V_STEP 25

#define CMD_RATE 40
#define FEEDBACK_RATE 40

#define MSG_SIZE 10

#define POLY 0x8408

#define TURN_SPEED 100
#define BEND_SPEED_INNER 55
#define BEND_SPEED_OUTER 250
#define BASE_SPEED 50
#define SPEED_GAIN 2

#define CMD_MSG_TIMEOUT_DURATION 100


#define SONIC_NUM 6
#define MAX_DISTANCE 255

#define STOP_DISTANCE 12
#define TURN_RIGHT_DISTANCE 30
#define TURN_LEFT_DISTANCE 25
#define MAX_WALL_DISTANCE 15
#define IDEAL_WALL_DISTANCE 13
#define MIN_WALL_DISTANCE 11



NewPing sonics_[SONIC_NUM] = {NewPing( 3,  3, MAX_DISTANCE),
                              NewPing(11, 11, MAX_DISTANCE),
                              NewPing(A2, A2, MAX_DISTANCE),
                              NewPing(A3, A3, MAX_DISTANCE),
                              NewPing(A4, A4, MAX_DISTANCE),
                              NewPing(A5, A5, MAX_DISTANCE),
                             };

DualVNH5019MotorShield md;


unsigned long next_cmd_time_;
unsigned long next_feedback_time_;
unsigned long prev_cmd_msg_time_;
int m1_cmd_ = 0;
int m2_cmd_ = 0;
int target_v1_ = 0;
int target_v2_ = 0;
char rx_buffer_[MSG_SIZE];
int next_write_ = 0;
bool msg_complete_ = false;




void stopIfFault()
{
  if (md.getM1Fault())
  {
    Serial.println("M1 fault");
    while (1);
  }
  if (md.getM2Fault())
  {
    Serial.println("M2 fault");
    while (1);
  }
}

int calculateCommand(int current_speed, int target_speed)
{
  int error;
  int command;

  // Make sure target is within legal range
  if (abs(target_speed) > V_MAX)
  {
    target_speed = V_MAX * (target_speed / abs(target_speed));
  }

  // Calculate error
  error = target_speed - current_speed;

  if (abs(error) < V_STEP)
  {
    command = target_speed;
  }
  else
  {
    command = current_speed + V_STEP * (error / abs(error));
  }

  return command;

}

// Checksum
unsigned short crc16(char *data_p, unsigned short length)
{
  unsigned char i;
  unsigned int data;
  unsigned int crc = 0x0000;

  if (length == 0)
    return (~crc);

  do
  {
    for (i = 0, data = (unsigned int)0xff & *data_p++;
         i < 8;
         i++, data >>= 1)
    {
      if ((crc & 0x0001) ^ (data & 0x0001))
        crc = (crc >> 1) ^ POLY;
      else  crc >>= 1;
    }
  } while (--length);


  return (crc);
}

void stop_robot() {
  md.setM1Speed(0);
  md.setM2Speed(0);
  stopIfFault();
  delay(50);
}

void drive_forwards(int forwards_speed) {
  md.setM1Speed(forwards_speed);
  md.setM2Speed(forwards_speed);
  stopIfFault();
  delay(10);
}

void adjust_left(int forwards_speed, int correction_speed) {
  md.setM1Speed(correction_speed);
  md.setM2Speed(forwards_speed);
  stopIfFault();
  delay(10);

}
void adjust_right(int forwards_speed, int correction_speed) {
  md.setM1Speed(forwards_speed);
  md.setM2Speed(correction_speed);
  stopIfFault();
  delay(10);

}

void turn_left() {
  md.setM1Speed(-TURN_SPEED);
  md.setM2Speed(TURN_SPEED);
  stopIfFault();
  delay(50);
}
/*
void turn_right_1() {
  md.setM1Speed(TURN_SPEED);
  md.setM2Speed(-TURN_SPEED);
  stopIfFault();
  delay(500);
}
*/
void turn_right_2() {
  md.setM1Speed(TURN_SPEED);
  md.setM2Speed(-TURN_SPEED);
  stopIfFault();
  delay(100);
}

void check_left () {
      int sonic_5 = sonics_[4].ping_cm();
      int sonic_6 = sonics_[5].ping_cm();
      sonic_5 = sonic_5;
      sonic_6 = sonic_6;

      Serial.println(sonic_5);
      Serial.println(sonic_6);
}
/*
void turn_robot(int sonic_5, int sonic_6) {

 // if(sonic_5 > 40 or sonic_6 > 40) {
    turn_right();
    Serial.println("Turn right");
    delay(10);
}
*/
 /* }
  else {
    turn_left();
    Serial.println("Turn left");
    delay(150);
  }
}
*/
void bend_left () {
  md.setM1Speed(BEND_SPEED_INNER);
  md.setM2Speed(BEND_SPEED_OUTER);
  stopIfFault();
  delay(10);
}



void setup()
{
  //Setting up pin 13 to start and stop program from raspi.

  pinMode(13, INPUT);
  Serial.begin(115200);
  md.init();
  next_cmd_time_ = millis();
  next_feedback_time_ = millis();
  prev_cmd_msg_time_ = millis() + CMD_MSG_TIMEOUT_DURATION;
}

void loop() {

  int sonic_1 = sonics_[0].ping_cm();
  int sonic_2 = sonics_[1].ping_cm();
  int sonic_3 = sonics_[2].ping_cm();
  int sonic_4 = sonics_[3].ping_cm();
  int sonic_5 = sonics_[4].ping_cm();
  int sonic_6 = sonics_[5].ping_cm();

  sonic_1 = constrain(sonic_1, 9, 150);
  sonic_2 = constrain(sonic_2, 9, 150);
  sonic_3 = constrain(sonic_3, 2, 80);
  sonic_4 = constrain(sonic_4, 2, 80);
  sonic_5 = constrain(sonic_5, 2, 80);
  sonic_6 = constrain(sonic_6, 2, 80);



  int dist_left = int((sonic_5 + sonic_6 ) / 2);
  int dist_right = int((sonic_3 + sonic_4 ) / 2);
  int dist_front = int((sonic_1 + sonic_2 ) / 2);
  //distance from ideal wall distance in decimal.
  int dist_from_ideal = abs((dist_left - IDEAL_WALL_DISTANCE) / IDEAL_WALL_DISTANCE);
  int diff_left = abs(sonic_5 - sonic_6);
  //Angle related to left wall in degrees
  int angle_left = int((diff_left / 20) * 90);

  int forwards_speed = int((dist_front * SPEED_GAIN) + BASE_SPEED);
  int correction_speed = int(forwards_speed * (1 - dist_from_ideal));


  if (sonic_1 < STOP_DISTANCE or sonic_2 < STOP_DISTANCE) {
    stop_robot();
    stop_robot();
    while (sonic_5 < 30 or sonic_6 < 30){
      turn_right_2();
      int sonic_5 = sonics_[4].ping_cm();
      int sonic_6 = sonics_[5].ping_cm();
      sonic_5 = sonic_5;
      sonic_6 = sonic_6;

      Serial.println(sonic_5);
      Serial.println(sonic_6);
      Serial.println("Turn right loop");
      if (sonic_5 < TURN_LEFT_DISTANCE or sonic_6 < TURN_LEFT_DISTANCE){
        break;
      }
    }
    }
   else if (sonic_5 > TURN_LEFT_DISTANCE) {
    bend_left();
    Serial.println("Bend left");
  }
  else {
    if (sonic_5 > MAX_WALL_DISTANCE) {
      adjust_left(forwards_speed, correction_speed);
      Serial.println("Adjust left");
    }
    else if (dist_left < MIN_WALL_DISTANCE) {
      adjust_right(forwards_speed, correction_speed);
      Serial.println("Adjust right");
    }
    else {
      drive_forwards(forwards_speed);
      Serial.println("Drive forwards");
    }
  }

  Serial.println("Sonic nr. 1 distance is:");
  Serial.println(sonic_1);
  Serial.println("Sonic nr. 2 distance is:");
  Serial.println(sonic_2);
  Serial.println("Sonic nr. 3 distance is:");
  Serial.println(sonic_3);
  Serial.println("Sonic nr. 4 distance is:");
  Serial.println(sonic_4);
  Serial.println("Sonic nr. 5 distance is:");
  Serial.println(sonic_5);
  Serial.println("Sonic nr. 6 distance is:");
  Serial.println(sonic_6);

  delay(50);

}
