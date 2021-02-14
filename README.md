# Autonomous-drone
mission planner kurulumu için;

sudo apt-get install mono-complete festival (.exe dosyası çalıştırmak için)

mono MissionPlanner.exe (/MissionPlanner-1.3.50 klasörün içinde)

gerekli kütüphaneler:

pip install mavproxy

pip install dronekit

pip install dronekit-sitl

simülasyonu başlatmak için :

dronekit-sitl copter

mavproxy.py --master tcp:127.0.0.1:5760 --out udp:127.0.0.1:14551 --out udp:(ip address):14550

sonra mission planner ekranında udp port 14550 seçilip connect yapılır


basic.py --> kare şeklinde yol çizdiren kod

goto.py --> dronekit simple_goto ile koordinatları bilinen noktaya gitmeyi sağlayan komut ile oluşturulan görev 

salyangoz.py --> açı değerlerini güncelleyerek çembersel rota oluşturan kod

teknomission.py --> yol planı(düzlük+çember) içinde çember çizdiren kod (goto ile)

