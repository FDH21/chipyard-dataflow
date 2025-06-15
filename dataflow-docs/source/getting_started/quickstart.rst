.. _quickstart:

快速开始
==========

使用Chipyard-dataflow 十分简单：

1. 我们的功能核设计基于 Gemmini_ 进行二次开发。

.. _Gemmini: https://github.com/ucb-bar/gemmini/ 


每次运行时初始化环境变量

.. code-block:: console

    cd /path/to/chipyard-dataflow
    source env.sh


编译
------------

.. code-block:: console

    cd generators/gemmini
    git submodule update --init --recursive 
    ./scripts/setup-paths.sh
    ./scripts/build-verilator.sh

    cd software/gemmini-rocc-tests
    ./build.sh


复制脚本
------------

.. code-block:: console

    chmod +x copy2build.sh
    ./copy2build.sh
    chmod +x ./test_bare.sh 
    chmod +x ./test_multi.sh

.. note::
    每次删除build文件后，都需要重新执行./copy2build.sh。

    ./test_bare.sh 用于生成baremetal程序，所有的可执行文件程序都要写在test_bare.sh中。
    
    ./test_multi.sh 用于生成多核程序，所有的可执行文件程序都要写在test_multi.sh中。

    

运行
-----------

.. code-block:: console

    ./test_bare.sh

    cd /path/to/gemmini

    chmod +x ./scripts/fix-dramsim-path.sh
    ./scripts/fix-dramsim-path.sh
    ./scripts/run-verilator.sh --debug vm_multi_ls_vs_sr_5c




