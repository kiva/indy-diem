git clone https://github.com/diem/diem.git
cd diem
./scripts/dev_setup.sh
source ~/.cargo/env


cargo run -p diem-node -- --test