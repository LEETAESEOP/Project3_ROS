#include "ros/ros.h" // ROS 헤더파일
#include  "topic_tutorial/my_msg.h" // my.msg 메시지 헤더파일
                                    // 빌드 후 자동 생성


class Myclass
{

    public:
        Myclass();
        void run();


    private:
        ros::NodeHandle nh;
        ros::Publisher pub;
        int cnt = 0;
        yh_sum::yh_sum_msg msg;

};


Myclass::Myclass()
{
    nh.advertise<topic_tutorial::my_msg>("my_topic", 100);
}

void Myclass::run()
{
    
        msg.stamp   = ros::Time::now();              // 현재 시간을 msg의 stamp에 담는다.
        msg.data    = cnt;                          // cnt의 변수값을 msg의 data에 담는다.
        cnt++; 
        my_pub.publish(msg);                        // my_pub이 msg를 퍼블리시 한다.
}

int main(int argc, char ** argv) // 로스에서는 argv 필수
{
    ros::init(argc, argv, "my_publisher"); // 노드이름 초기화
    Myclass my_class;
    ros::Rate loop_rate(5);
    while(ros::ok()) // 로스가 켜져있다면 계속 반복
    {
        my_class.run();
        loop_rate.sleep();
    }   
    return 0;
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main(int argc, char ** argv) // 로스에서는 argv 필수
{
    ros::init(argc, argv, "my_publisher"); // 노드이름 초기화
    ros::NodeHandle nh; //  ROS 시스템과 통신을 위한 노드 핸들 선언
    
    // 퍼블리셔 선언
    // 패키지(topic_tutorial)의 메세지 파일(my_msg)을 이용한 퍼블리셔
    // 퍼블리셔(my_pub)를 작성한다. 토픽은 (my_topic)이며,
    // 퍼블리셔큐(queue) 사이즈를 100개로 설정한다.
    ros::Publisher my_pub = nh.advertise<topic_tutorial::my_msg>("my_topic", 100);

    ros::Rate loop_rate(5); // 루프 주기를 10hz로 설정한다.

    topic_tutorial::my_msg msg;
    
    int cnt = 0;

    while(ros::ok()) // 로스가 켜져있다면 계속 반복
    {
        msg.stamp   = ros::Time::now();              // 현재 시간을 msg의 stamp에 담는다.
        msg.data    = cnt;                          // cnt의 변수값을 msg의 data에 담는다.
        cnt++; 
        my_pub.publish(msg);                        // my_pub이 msg를 퍼블리시 한다.
        loop_rate.sleep();                          // 위에서 설정한 주기에 따라 sleep 한다.
    }

    return 0;
}

