# ROS + Gazeboのシミュレーション  

## 必要環境  
ROS kineticのインストール  
  
また下記のコマンドでros-controlをインストールする。  
'sudo apt-get install ros-kinetic-ros-control ros-kinetic-ros-controllers'  
  


## 参考にしたページ  
・シミュレーション環境の準備  
http://bril-tech.blogspot.com/2016/10/ros3.html  
  
・シミュレーションへのLiDAR、Camaraの適用  
http://gazebosim.org/tutorials?tut=ros_gzplugins  
  


## インストール  
下記のコマンドによりROSのワークスペースにこのパッケージをダウンロードする。  
cd catkin_ws/src  
git clone https://github.com/IgarashiBME/sim_create  
  


## 使用方法  
### 自律走行(move_base)  
下記のコマンドを実行する。  
navi_sim_create.shが存在するディレクトリに移動し、下記のコマンドを実行する。  
./navi_sim_create.sh  
  


### 2Dマッピング(gmapping)  
ナビゲーションのために使うマップを自分で作りたい場合は下記を実行する。  
  
gmapping_sim_create.shが存在するディレクトリに移動し、下記のコマンドを実行する。  
./gmapping_sim_create.sh  
  
rosrun sim_create key_teleop.pyが実行されているターミナルで  
w,a,s,dキーを押すことで機体を動かせる。機体を動かせば、マッピングが行われていく。  
  
マップのセーブは下記のコマンドで行う。  
rosrun map_server map_saver  
  
自作のgazebo worldと2Dマップをmove_baseに適用する際は、下記のファイルの参照先に気をつける。  
・ launch/movebase.launch  
<node name="map_server" pkg="map_server" type="map_server" args="$(find sim_create)/maps/iga.yaml"/>  
  
・ launch/gazebo.launch  
<arg name="world_name" value="$(find sim_create)/world/iga.world" />  
  
・ マップのセーブの際に生成されたyamlファイル  
pgmファイルの読み込み先に気をつける。  
