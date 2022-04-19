#include "ros/ros.h" // ROS 헤더파일
#include  "yh_tutorial_1/yh_msg_1.h" // my.msg 메시지 헤더파일
                                    // 빌드 후 자동 생성 // my.msg 메시지 헤더파일
                                    // 빌드 후 자동 생성

// 메시지 콜백함수, 서브스크라이버가 메시지를 수신했을 때 동작하는 함수이다.
// 입력메시지로는 패키지이름(topic_tutorial)의 메시지 이름(my_msg)을 받도록 되어있다.
void msgCallback(const yh_tutorial_1::yh_msg_1::ConstPtr& msg)
{
    // class Bclass{ int c = 10;}
    // Bclass b;
    // Bclass *a = &b;
    // print("%d", a->c);
    // print("%d", *a.c);
    // *a.c 는 a->c 와 같다.

    ROS_INFO("receive msg =%d", msg->stamp.sec);    // stamp.sec를 표시한다.
    ROS_INFO("receive msg =%d", msg->stamp.nsec);   // stamp.nsec를 표시한다.
    ROS_INFO("receive msg =%d", msg->data);         // data를 표시한다.
}

// 메인 함수
int main(int argc, char ** argv)
{
    ros::init(argc, argv, "yh_sub_1"); // 노드 이름 초기화
    ros::NodeHandle nh; // ROS 시스템과 통신을 위한 노드 핸들 선언

    // 서브스크라이버 선언
    // 패키지(topic_tutorial)의 메시지(my_msg)을 이용한 서브스크라이버(my_sub)를 작성한다.
    // 토픽명은 (my_topic)이며, 서브스크라이버큐(queue)의 사이즈를 100으로 설정한다.
    // 콜백 함수명은 (msgCallback)이다.
    ros::Subscriber my_sub = nh.subscribe("yh_topic_1", 100, msgCallback);

    // spin = 제자리에서 돌며 대기하는 함수
    ros::spin();

    return 0;
}