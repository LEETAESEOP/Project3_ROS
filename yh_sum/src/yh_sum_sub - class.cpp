#include "ros/ros.h"                // ROS 헤더파일
#include "topic_tutorial/my_msg.h"  // my.msg 메시지 헤더파일
                                    // 빌드 후 자동 생성

// 메시지 콜백함수, 서브스크라이버가 메시지를 수신했을 때 동작하는 함수이다.
// 입력메시지로는 패키지이름(topic_tutorial)의 메시지 이름(my_msg)을 받도록 되어있다.


class MyClass
{
//퍼블릭에는 함수가들어가고, 외부접근 가능
    public:
        MyClass()
        {
            sub = nh.subscribe("yh_sum_topic", 100 &MyClass::msgCallback, this);
        }

        void msgCallback(const topic_tutorial::my_msg::ConstPtr& msg)
        {
            printf("%d\n", old_data + msg->data);
            old_data = msg -> data;
        }

//private에는 변수가 들어감, 외부접근 불가능
    private:
        ros::NodeHandle nh;
        ros::Subscriber sub;
        int old_data = 0;


};

int main(int argc, char ** argv)
{
    ros::init(argc, argv, "my_subscriber"); // 노드 이름 초기화
    my_class = MyClass();
    ros::spin();

    return 0;
}


///////////////////////////////////////////////////////////////////////////

int old_data = 0;

void msgCallback(const topic_tutorial::my_msg::ConstPtr& msg)
{
    printf("%d\n", old_data + msg->data);
    old_data = msg -> data;
}


int main(int argc, char ** argv)
{
    ros::init(argc, argv, "my_subscriber"); // 노드 이름 초기화
    ros::NodeHandle nh; // ROS 시스템과 통신을 위한 노드 핸들 선언

    // 서브스크라이버 선언
    // 패키지(topic_tutorial)의 메시지(my_msg)을 이용한 서브스크라이버(my_sub)를 작성한다.
    // 토픽명은 (my_topic)이며, 서브스크라이버큐(queue)의 사이즈를 100으로 설정한다.
    // 콜백 함수명은 (msgCallback)이다.
    ros::Subscriber my_sub = nh.subscribe("my_topic", 100, msgCallback);

    // spin = 제자리에서 돌며 대기하는 함수
    ros::spin();

    return 0;
}