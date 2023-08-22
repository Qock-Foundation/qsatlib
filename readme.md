## Clone qsatlib

    git clone https://github.com/Qock-Foundation/qsatlib

## Install dependency: caqe

    git clone https://github.com/ltentrup/caqe
    cd caqe
    sudo apt install -y cargo
    git fetch --force --update-head-ok 'https://github.com/rust-lang/crates.io-index' 'refs/heads/master:refs/remotes/origin/master' 'HEAD:refs/remotes/origin/HEAD'
    cargo build --release
    cd ..