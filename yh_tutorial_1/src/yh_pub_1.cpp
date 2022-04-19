#include "ros/ros.h" // ROS 헤더파일
#include  "yh_tutorial_1/yh_msg_1.h" // my.msg 메시지 헤더파일
                                    // 빌드 후 자동 생성


// 메인 함수
int main(int argc, char ** argv) // 로스에서는 argv 필수
{
    ros::init(argc, argv, "yh_pub_1"); // 노드이름 초기화
    ros::NodeHandle nh; //  ROS 시스템과 통신을 위한 노드 핸들 선언
    
    // 퍼블리셔 선언
    // 패키지(yh_tutorial)의 메세지 파일(yh_msg_1)을 이용한 퍼블리셔
    // 퍼블리셔(my_pub)를 작성한다. 토픽은 (yh_topic_1)이며,
    // 퍼블리셔큐(queue) 사이즈를 100개로 설정한다.
    ros::Publisher my_pub = nh.advertise<yh_tutorial_1::yh_msg_1>("yh_topic_1", 100);

    ros::Rate loop_rate(50); // 루프 주기를 10hz로 설정한다.

    yh_tutorial_1::yh_msg_1 msg;
    int cnt = 0;

    while(ros::ok()) // 로스가 켜져있다면 계속 반복
    {
        msg.stamp   = ros::Time::now();              // 현재 시간을 msg의 stamp에 담는다.
        msg.data    = cnt;                          // cnt의 변수값을 msg의 data에 담는다.
        ROS_INFO("send msg = %d", msg.stamp.sec);   // stamp.sec를 표시한다.
        ROS_INFO("send msg = %d", msg.stamp.nsec);  // stamp.nsec를 표시한다.
        ROS_INFO("send msg = %d", msg.data);        // data를 표시한다.
        cnt++; 
        my_pub.publish(msg);                        // my_pub이 msg를 퍼블리시 한다.
        loop_rate.sleep();                          // 위에서 설정한 주기에 따라 sleep 한다.
    }

    return 0;
}

    // :: 이란 

    // 파이썬
    // import cv2
    // cv2.imread()

    // ROS
    // import cv2
    // cv2::imread()