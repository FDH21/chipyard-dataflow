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

    cd build
    ./npusim --config-file ../llm/test/config_pd_sim.json

其中 ``config_pd_sim.json`` 为一个配置文件，你可以根据你的需求进行修改。

.. note::
    在继续这个教程之前，请确保你完成了 :ref:`安装指南 <installation>`, 并确保配置了相关的环境变量。




.. _configuration-fields:

配置字段说明
--------------

以下是对配置文件中各个字段的详细说明：

通用控制参数
~~~~~~~~~~~~~

random : bool, optional
  默认为 false，是否启用工作核随机排列，会反应在生成的数据流图上。

pipeline : int, optional
  默认为 1。如果该值大于 1，则开启 pipeline 模式，具体表现为 memInterface 会将 source 字段中的 start data 复制对应次数连续发送给工作核，在 memInterface 接收到 pipeline 对应数量的 DONE 信号后，程序结束。
  简单的来说，pipeline 的次数就是 下发的 input 请求的次数。

sequential : bool, optional
  默认为 false。如果为 true，则开启 sequential 模式，具体表现为 memInterface 会在接收到每一个 DONE 信号之后，依次发送 source 字段数组下的所有 start data，每次只发送数组中的一个元素，在发送完毕并接收到最后的 DONE 信号之后，程序结束。

  .. note::
     ``sequential`` 和 ``pipeline`` 模式不能同时启用。目前 ``sequential`` 仅用于 pd 阶段的模拟。
  .. code-block:: json

    "source": [
      {
        "dest": 0,
        "size": "BTC"
      },
      {
        "dest": 3,
        "size": "C",
        "loop": "L"
      }
    ]

  上面的配置表示 1次0，L次3 模拟 ``prefill`` 和 ``decoding`` 阶段的 input 下发

vars : dict
  记录数值的键值对，在下方的配置中出现的所有字符串可以在这里转换成对应的数字。

  
  .. note::
     如果配置 sram 的地址的话，需要 1024 个元素对齐，即所需要的数据量除以1024（这里不会乘上每个数据的BYTE数，或默认为INT8存储所需要的地址偏移）。
     这样的设计可以避免数据类型变化对地址索引的影响。


source : list of dicts
  一个数组，记录了所有 start data 的相关信息。如果不为 sequential 模式，则在程序开始时、发送完所有的 prepare data 之后，memInterface 会一次性发送所有的 start data。

  每个字典包含以下字段：

  - dest : int
      start data 发送的目的地核编号。
  - size : string
      start data 的大小，在 ``vars`` 中查找对应值。
  - loop : int, optional
      默认为 1。需要循环发送本 start data 的次数，**仅在 sequential 模式下使用**。

chip : list of dicts
  记录拓扑配置，虽然是数组但目前仅使用数组的第一个元素。

  每个字典包含以下字段：

  - GridX : int
      X 维度计算核的个数。
  - GridY : int
      Y 维度计算核的个数（目前需要强制等同于 GridX）。
  - cores : list of dicts
      计算核相关配置，每一个数组元素代表一个核。

core 配置
~~~~~~~~~~~~~~~~~

每个 core 包含以下字段：

- id : int
    计算核 ID。

- prim_prefill : bool, optional
    默认为 false。该核是否需要支持无限循环执行，在 pipeline 模式下需要开启。

- prim_copy : int, optional
    默认为 -1（不开启）。该核是否需要完全复制另一个核 worklist 中的原语。但需注意如果要复制的话，还是需要在自己的 worklist 中注明对应的 cast、recv_cnt 和 recv_tag。
    该数值表示复制哪一个 core_id 的原语组

.. raw:: html

    <!-- 引入 Prism.js 主题样式 -->
    <link href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.css" rel="stylesheet">
    <!-- 引入 Prism.js 核心库 -->
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
    <!-- 引入 JSON 语法支持组件 -->
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-json.min.js"></script>

    <style>
        .advanced-tab-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
            padding: 20px;
            overflow: hidden;
        }

        .tab-buttons {
            display: flex;
            list-style: none;
            padding: 0;
            margin: 0;
            border-bottom: 2px solid #eaeaea;
        }

        .tab-buttons li {
            cursor: pointer;
            padding: 12px 24px;
            font-weight: 500;
            color: #555;
            transition: all 0.3s ease;
            border-radius: 8px 8px 0 0;
            position: relative;
        }

        .tab-buttons li:hover {
            background-color: #f5f5f5;
        }

        .tab-buttons li.active {
            color: #007BFF;
            border-bottom: 3px solid #007BFF;
            background-color: #fff;
            transform: translateY(-1px);
        }

        .tab-content {
            padding: 24px 20px;
            background-color: #fff;
            min-height: 120px;
            border-radius: 0 0 10px 10px;
            transition: opacity 0.3s ease, transform 0.3s ease;
            opacity: 1;
            transform: translateY(0);
        }

        .tab-content.hidden {
            display: none;
            opacity: 0;
            transform: translateY(10px);
        }

        mark, .highlight {
            background-color: #f0f0f0; /* 浅灰色背景 */
            color: #990066; /* 紫红色字体 */
            font-family: 'Courier New', Courier, monospace; /* 等宽字体 */
            padding: 1px 1px;
            border-radius: 3px;
            white-space: nowrap;
            /* 轻微立体效果 */
            background: linear-gradient(145deg, #ececec, #f8f8f8); /* 更柔和的渐变 */
            box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1), /* 更浅的外阴影 */
                        -1px -1px 2px rgba(255, 255, 255, 0.3); /* 更浅的内阴影 */
        }

        
        

        /* Code block typography and alignment */
        code.language-json {
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.5;
            color: rgb(124, 124, 19); /* Light text for contrast */
            display: block; /* Ensure code behaves as a block element */
            text-align: left; /* Explicitly align text to the left */
        }

        /* Syntax highlighting for JSON (works with Prism.js or similar libraries) */
        code.language-json .key {
            color: #ff79c6; /* Pink for keys */
        }
        code.language-json .string {
            color: #bd93f9; /* Yellow for strings */
        }
        code.language-json .number {
            color: #bd93f9; /* Purple for numbers */
        }
        code.language-json .punctuation {
            color:rgb(124, 124, 19); /* White for punctuation */
        }

        /* 自定义 note 样式 */
        .custom-note {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px 20px;
            margin: 15px 0;
            border-radius: 4px;
            font-size: 0.95em;
            color: #0d47a1;
            line-height: 1.5;
            position: relative;
        }

        .custom-note:before {
            content: "Note";
            position: absolute;
            top: -1px;
            left: -15px;
            background-color: #2196f3;
            color: white;
            padding: 2px 8px;
            font-size: 0.8em;
            font-weight: bold;
            border-radius: 4px 0 4px 0;
        }


            /* 自定义 TODO 样式 */
        .custom-todo {
            background-color: #ffebee; /* 浅红色背景 */
            border-left: 4px solid #f44336; /* 红色边框 */
            padding: 15px 20px;
            margin: 15px 0;
            border-radius: 4px;
            font-size: 0.95em;
            color: #b71c1c; /* 深红色文字 */
            line-height: 1.5;
            position: relative;
            list-style-type: disc;
        }

        .custom-todo:before {
            content: "TODO"; /* 改为 TODO */
            position: absolute;
            top: -1px;
            left: -15px;
            background-color: #f44336; /* 红色背景 */
            color: white;
            padding: 2px 8px;
            font-size: 0.8em;
            font-weight: bold;
            border-radius: 4px 0 4px 0;
        }


    

    </style>

    <div class="advanced-tab-container">
        <ul class="tab-buttons">
            <li class="active" onclick="switchTab(event, 'contentA')">选项 A</li>
            <li onclick="switchTab(event, 'contentB')">选项 B</li>
        </ul>

        <div id="contentA" class="tab-content">
            <h4>Worklist 配置说明</h4>
            <ul>
                <li><strong>worklist</strong> : list of dicts
                    <p>按照顺序指示计算核需要完成的工作。</p>
                    <p>每个 worklist 元素包含以下字段：</p>
                    <ul>
                        <li><strong>recv_cnt</strong> : int
                            <p>在执行这个 <mark>worklist</mark> 数组元素的原语之前，需要接收到多少个对应 <mark>tag</mark> 的 <mark>SEND_DRAM</mark> 原语的 <mark>END_packet</mark>。</p>
                        </li>
                        <li><strong>recv_tag</strong> : int, optional
                            <p>默认值为此计算核 ID。被此 worklist 数组元素所接受的 SEND msg 的 tag。不是此 tag 的消息不会被接收。</p>
                            
                            <!-- 这里插入自定义 note -->
                            
                            <div class="custom-note">
                                在配置文件时，需要注意每一个核的第一个 worklist 数组元素的recv_tag 必须与此计算核的 ID 相同（可省略）。
                                如果在后续的 worklist 元素中，会收到超过其他发送核给它发送的SEND_DRAM包，则需要分配与该CoreID <mark>不同的</mark> recv_tag作为标识，
                                同时不同接收核的recv_tag也需要 <mark>互异</mark> ，来自同一发送核的recv_tag可以 <mark>一致</mark> ，推荐在原ID基础上增加一个较大的值。
                            </div>

                                <pre><code class="language-json">
    {
    // TP 2 主核的配置
    "worklist": [
        {
            "recv_cnt": 1,
            "cast": [
            {
                "dest": 1,
                "addr": 1000000
            }
            ],
            "prims": [
            ...
            ]
        },
        {
            "recv_cnt": 0,
            "cast": [],
            "prims": [
            ....
            
            ]
        },
        {
            "recv_cnt": 1,
            "recv_tag": 120,
            "cast": [
            {
                "dest": 1,
                "addr": 2000000
            }
            ],
            "prims": [
            ....
            ]
        },
        {
            "recv_cnt": 0,
            "cast": [],
            "prims": [
            .....
            ]
        },
        {
            "recv_cnt": 1,
            "recv_tag": 121,
            "cast": [
            {
                "dest": 2,
                "critical": true
            }
            ],
            "prims": [
            .....
            ]
        }
        ]
    
    // TP 2 从核的配置
    "worklist": [
        {
            "recv_cnt": 1,
            "cast": [
            {
                "dest": 0,
                "tag": 120,
                "addr": 1000000
            }
            ],
            "prims": [
            ...
            ]
        },
        {
            "recv_cnt": 1,
            "cast": [
            {
                "dest": 0,
                "tag": 121,
                "addr": 2000000
            }
            ],
            "prims": [
            ...
            ]
        }
        ]
    }
                            </code></pre>

                        <div class="custom-note">
                        <ul>
                            <li><strong>上述示例1</strong>，展示了一个 worklist 中有五组 prims，可以认为是在做tp并行是主核的配置。
                            其中第一组 recv_cnt 为1，表示需要接收一个 SEND_DRAM 的 END_packet，recv_tag 默认为本身 coreID。
                            后续的四组，如果 recv_cnt 不为0，因为需要接受从核发过来的数据，所以需要自定义的 recv_tag。
                            如果 recv_cnt 为0，则表示不需要接收SEND_DRAM的END_packet，也不需要设置 recv_tag。
                            </li>
                            <li><strong>上述示例2</strong>，展示的tp并行中从核的配置。因为只需要接受来自主核的数据，所以不需要设置 recv_tag。但是 cast 中的 tag 
                            需要和主核的 recv_tag 一致，否则会丢失数据。 </li>
                        </ul>
                        </div>
                            
                        <div class="custom-todo">
                                注意现在cast中的addr地址还有问题，理论上应该指向sram的地址。
                        </div>

                        

                        </li>
                        <li><strong>cast</strong> : list of dicts
                            <p>在此 worklist 元素的所有原语完成之后，需要将结果发送到哪些核。</p>
                            <p>每个 cast 元素包含以下字段：</p>
                            <ul>
                                <li><strong>dest</strong> : int
                                    <p>目标核 ID。</p>
                                </li>
                                <li><strong>addr</strong> : int
                                    <p>目标核 DRAM 偏移量。</p>
                                
                                </li>
                                <li><strong>tag</strong> : int
                                    <p>目标核的recv_tag， 默认是目标核 ID。</p>
                                
                                </li>

                            </ul>
                        </li>
                        <li><strong>prims</strong> : list of dicts
                            <p>此 worklist 元素需要完成的所有 comp 原语。</p>
                            <p>每个 prim 元素包含以下字段：</p>
                            <ul>
                                <li><strong>type</strong> : string
                                    <p>原语类型（需填写指定字符串）。</p>
                                
                                </li>
                                <li><strong>vars</strong> : string or int
                                    <p>vars 处填写原语需要的参数名，值可以用 string 在 通用控制参数中的 vars 字段查找，也可以填写数字。</p>
                                
                                </li>
                                <li><strong>sram_address</strong> : dict
                                    <ul>
                                        <li><strong>indata</strong> : string
                                            <p>此原语的输入位于 SRAM 的什么标签处。</p>
                                            <div class="custom-note">
                                                如果需要从 DRAM 获取，则必须先写 <code>dram_label</code>，随后在一个空格后加上从 DRAM 
                                                读取出数据后存放在 SRAM 中的标签名。如果原语会有几部分的输入，
                                                则统一用一个空格隔开。
                                            </div>
                                            
                                            
                                            <pre><code class="language-json">
    {// 用dram_label 修饰conv1_in 表示从 dram 中取数到 sram
        "sram_address": {
            "indata": "dram_label conv1_in",
            "outdata": "conv1_out"
        },
    }
                                            </code></pre>
                                            
                                            <div class="custom-note">

                                             <ul>
                                                <li>对于上一个核路由传进来的输入数据（保存在 SRAM 上），则在 <code>sram_address</code> 中用 <code>input_label</code> 表示。</li>
                                                <li>一般来说，算子的输入张量，用完即可清除，但是对于类似 residual 算子，一个输入张量可能会被后续张量使用，需要在 <code>residual1_in</code> 前加上 <code>_residual1_in</code>。</li>

                                            </ul>
                                
                                            </div>
                                            <pre><code class="language-json">
    {// input_label 前面下划线表示，表示此输入张量在 SRAM 还未使用完，不可以被清除。
        "sram_address": {
            "indata": "_input_label",
            "outdata": "layernorm1_out"
        },
    }
                                            </code></pre>
                                            
                                        </li>
                                        <li><strong>outdata</strong> : string
                                            <p>此原语的输出会保存在 SRAM 的什么标签处。</p>
                                        </li>
                                    </ul>
                                </li>
                                <li><strong>dram_address</strong> : dict
                                    <p>此原语在 DRAM 中存储相关。</p>
                                    <ul>
                                        <li><strong>input</strong> : string or int, optional
                                            <p>默认为 0。此原语输入在 DRAM 中的位置。</p>
                                        </li>
                                        <li><strong>data</strong> : string or int, optional
                                            <p>默认为 0。此原语数据、权重在 DRAM 中的位置，如果为 -1，则表示此原语不需要权重的数据。</p>
                                        </li>
                                        <li><strong>out</strong> : string or int, optional
                                            <p>默认为 0。此原语输出在 DRAM 中的位置。</p>
                                        </li>

                                        <div class="custom-todo">
                                                spill back 的 dram 地址现在都是inp_address。
                                        </div>

                                        
                                    </ul>
                                </li>
                            </ul>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>

        <div id="contentB" class="tab-content hidden">
            <h4>这是选项 B 的内容区域</h4>
            <p>你可以在这里放置其他配置项、代码示例、流程图说明等。</p>
        </div>

        <script>
            function switchTab(evt, tabName) {
                var i, tabcontent, tablinks;

                // 隐藏所有内容
                tabcontent = document.querySelectorAll(".tab-content");
                for (i = 0; i < tabcontent.length; i++) {
                    tabcontent[i].classList.add("hidden");
                }

                // 移除 active 类
                tablinks = document.querySelectorAll(".tab-buttons li");
                for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].classList.remove("active");
                }

                // 显示当前内容并添加 active 类
                document.getElementById(tabName).classList.remove("hidden");
                evt.currentTarget.classList.add("active");
            }

            // 页面加载时自动点击第一个 tab
            document.addEventListener("DOMContentLoaded", function() {
                document.querySelector('.tab-buttons li.active').click();
            });
        </script>
    </div>

- worklist : list of dicts
    按照顺序指示计算核需要完成的工作。

    每个 worklist 元素包含以下字段：

    - recv_cnt : int
        在执行这个 worklist 数组元素的原语之前，需要接收到多少个对应 tag 的 SEND_DRAM 原语的 end packet。

    - recv_tag : int, optional
        默认值为此计算核 id。被此 worklist 数组元素所接受的 SEND msg 的 tag。不是此 tag 的消息不会被接收。
        
        .. note::
           在配置文件时，需要注意每一个核的第一个 worklist 数组元素的 tag 必须与此计算核的 id 相同。且在后续的 worklist 元素中，tag 必须与此计算核的 id 不同，推荐在原 id 基础上增加一个较大的值。

    - cast : list of dicts
        在此 worklist 元素的所有原语完成之后，需要将结果发送到哪些核。

        每个 cast 元素包含以下字段：

        - dest : int
            目标核 ID。
        - addr : int
            目标核 DRAM 偏移量。

    - prims : list of dicts
        此 worklist 元素需要完成的所有 comp 原语。

        每个 prim 元素包含以下字段：

        


        - type : string
            原语类型（需填写指定字符串）。

        - vars : string or int
            vars 处填写原语需要的参数名，值可以用 string 在 ``vars`` 字段查找，也可以填写数字。

        - sram_address : dict
            此原语在 SRAM 中存储相关。

            - indata : string
                此原语的输入位于 SRAM 的什么标签处。如果需要从 DRAM 获取，则必须先写 "dram_label"，随后在一个空格后加上从 DRAM 读取出数据后存放在 SRAM 中的标签名。如果原语会有几部分的输入，则统一用一个空格隔开。

                .. note::
                   - 对于上一个核路由传进来的输入数据（保存在 SRAM 上），则在 ``sram_address`` 中用 ``input_label`` 表示。
                   - 一般来说，算子的输入张量，用完即可清除，但是对于类似 residual 算子，一个输入张量可能会被后续张量使用，需要在 ``input_label`` 前加上 ``_input_label``。

            - outdata : string
                此原语的输出会保存在 SRAM 的什么标签处。

        - dram_address : dict
            此原语在 DRAM 中存储相关。

            - input : string or int, optional
                默认为 0。此原语输入在 DRAM 中的位置。

            - data : string or int, optional
                默认为 0。此原语数据、权重在 DRAM 中的位置，如果为 -1，则表示此原语不需要权重的数据。

            - out : string or int, optional
                默认为 0。此原语输出在 DRAM 中的位置。

        

