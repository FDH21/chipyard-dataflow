.. _installation:

安装指南
============

**Chipyard-dataflow** 是基于加州大学伯克利分校（UCB）Bar 实验室开发的开源框架 `Chipyard <https://github.com/ucb-bar/chipyard/tree/stable>`_  进行二次开发的仿真器，旨在增强其数据流处理能力，拓展原有系统的功能与应用场景。

相关文档
------------

详细信息可以参见官方文档 `Chipyard Documentation <https://chipyard.readthedocs.io/en/stable/>`_ 

这里提供了快速安装的教程


.. code-block:: console

    git clone https://github.com/FDH21/chipyard-dataflow
    conda activate base
    # skip firemarshal and firesim
    ./build-setup.sh riscv-tools  -s 6 -s 7 -s 8 -s 9

安装firemarshal（可略）

.. code-block:: console

    source env.sh
    cd ./software/firemarshal
    ulimit -Sn $(ulimit -Hn) 
    
    ./init-submodules.sh
    ./marshal build br-base.json

  