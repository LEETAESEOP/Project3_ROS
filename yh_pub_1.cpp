#include "ros/ros.h" // ROS 헤더파일
#include "yh_tutorial_1/yh_msg_1.h" // my_msg 메세지 헤더파일
                                   // 빌드 후 자동 실행
        // 앞에 패키지 이름, 뒤에 우리가 갖고올 헤더 이름

// 메인 함수
int main(int argc, char ** argv)
{   // init = initialize(?) 시작한다는 의미.
    ros::init(argc, argv, "yh_pub_1"); // 노드 이름 초기화
    // 노드를 통신을 통해 컨트롤 하기 위한 NodeHandle 선언. nh = 변수명(?)
    ros::NodeHandle nh; // ROS 시스템과 통신을 위한 노드 핸들 선언

    // 퍼블리셔 선언
    // 패키지 (topic_tutorial)의 메세지 파일 (my_msg)을 이용한 퍼블리셔 (my_pub)를 작성한다.
    // 토픽은 (my_topic)이며, 퍼블리셔큐(queue) 사이즈를 100개로 설정한다.
    ros::Publisher my_pub = nh.advertise<yh_tutorial_1::yh_msg_1>("yh_topic_1", 100);  // 퍼블리셔가 큐 형태로 subscriber로 밀어넣음. 그 사이즈가 100임.
    // 위 ros::Publisher=자료형    my_pub=변수명
    ros::Rate loop_rate(2); // 루프 주기를 2Hz로 설정한다.

    yh_tutorial_1::yh_msg_1 msg;
    int cnt = 0;

    // ros가 켜져있으면 True
    while (ros::ok())
    {
        msg.stamp = ros::Time::now(); // 현재 시간을 msg의 stamp에 담는다.
        msg.data = cnt; // cnt의 변수값을 msg의 data에 담는다.
        ROS_INFO("send msg = %d", msg.stamp.sec); // stamp.sec를 표시한다
        ROS_INFO("send msg = %d", msg.stamp.nsec); // stamp.nsec를 표시한다
        ROS_INFO("send msg = %d", msg.data); // data를 표시한다
        cnt ++;
        my_pub.publish(msg); // my_pub이 msg를 퍼블리시한다.
        loop_rate.sleep(); // 위에서 정한 주기에 따라 sleep 한다. (잠깐 멈추도록 함)
    }
    
    return 0;
    // return 0; 하면 프로그램 종료 의미
}


