TASK = "Train a generative model for both unconditional image generation and class-conditional generation. Diffusion-related or flow-related models are preferred."


DATASET = r"""
The dataset for both unconditional image generation and class-conditional generation is CIFAR-10. The downloaded dataset is in the directory `/workplace/dataset_candidate/cifar-10-python.tar.gz`, you can refer to its README.md in `/workplace/dataset_candidate/edm/README.md` when you need to process the dataset.
"""

BASELINE = r"""
• Diffusion models: Score SDE [11], DDPM [3], LSGM [12], EDM [4] and NCSN++-G [2].
• Distilled diffusion models: Knowledge Distillation [7], DFNO (LPIPS) [13] TRACT [1] and PD [8].
• Consistency models: CD (LPIPS) [10], CT (LPIPS) [10], iCT [9] , iCT-deep [9], CTM [5] and CTM [5] + GAN.
• Rectified flows: 1,2,3-rectified flow(+distill) [6].

References: 
[1] David Berthelot, Arnaud Autef, Jierui Lin, Dian Ang Yap, Shuangfei Zhai, Siyuan Hu, Daniel Zheng, Walter Talbott, and Eric Gu. Tract: Denoising diffusion models with transitive closure time-distillation. arXiv preprint arXiv:2303.04248, 2023.
[2] Chen-Hao Chao, Wei-Fang Sun, Bo-Wun Cheng, Yi-Chen Lo, Chia-Che Chang, Yu-Lun Liu, Yu- Lin Chang, Chia-Ping Chen, and Chun-Yi Lee. Denoising likelihood score matching for conditional score-based data generation. In ICLR. OpenReview.net, 2022.
[3] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. Advances in Neural Information Processing Systems, 33:6840–6851, 2020.
[4] Tero Karras, Miika Aittala, Timo Aila, and Samuli Laine. Elucidating the design space of diffusion- based generative models. arXiv preprint arXiv:2206.00364, 2022.
[5] Dongjun Kim, Chieh-Hsin Lai, Wei-Hsiang Liao, Naoki Murata, Yuhta Takida, Toshimitsu Ue- saka, Yutong He, Yuki Mitsufuji, and Stefano Ermon. Consistency trajectory models: Learning probability flow ode trajectory of diffusion. arXiv preprint arXiv:2310.02279, 2023.
[6] Xingchao Liu, Chengyue Gong, and Qiang Liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. arXiv preprint arXiv:2209.03003, 2022.
[7] Eric Luhman and Troy Luhman. Knowledge distillation in iterative generative models for improved sampling speed. arXiv preprint arXiv:2101.02388, 2021.
[8] Tim Salimans and Jonathan Ho. Progressive distillation for fast sampling of diffusion models. arXiv preprint arXiv:2202.00512, 2022.
[9] Yang Song and Prafulla Dhariwal. Improved techniques for training consistency models. arXiv preprint arXiv:2310.14189, 2023.
[10] Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. Consistency models. arXiv preprint arXiv:2303.01469, 2023.
[11] Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-based generative modeling through stochastic differential equations. arXiv preprint arXiv:2011.13456, 2020.
[12] Arash Vahdat, Karsten Kreis, and Jan Kautz. Score-based generative modeling in latent space. Advances in Neural Information Processing Systems, 34:11287–11302, 2021.
[13] Hongkai Zheng, Weili Nie, Arash Vahdat, Kamyar Azizzadenesheli, and Anima Anandkumar. Fast sampling of diffusion models via operator learning. arXiv preprint arXiv:2211.13449, 2022.
"""

COMPARISON = r"""
\begin{table*}[h]
\small
    \begin{minipage}[t]{0.49\linewidth}
	\caption{Unconditional generation on CIFAR-10.}
    \label{tab:cifar-10}
	\centering
	{\setlength{\extrarowheight}{0.4pt}
	\begin{adjustbox}{max width=\linewidth}
	\begin{tabular}{@{}l@{\hspace{-0.2em}}c@{\hspace{0.3em}}c@{}}
        \Xhline{3\arrayrulewidth}
	    METHOD & NFE ($\downarrow$) & FID ($\downarrow$) \\
        \\[-2ex]
        \multicolumn{3}{@{}l}{\textbf{Diffusion models}}\\\Xhline{3\arrayrulewidth}
        Score SDE & 2000 & 2.38 \\
        DDPM & 1000 & 3.17 \\
        LSGM  & 147 & 2.10 \\
        EDM 
         & 35 & 1.97   \\
        \multicolumn{3}{@{}l}{\textbf{Distilled diffusion models}}\\\Xhline{3\arrayrulewidth}
        Knowledge Distillation & 1 & 9.36 \\
        DFNO (LPIPS) & 1 & 3.78 \\
        TRACT & 1 & 3.78 \\
         & 2 & \textcolor{blue}{3.32} \\
        PD  & 1 & 9.12  \\
          & 2 & 4.51 \\
        \multicolumn{3}{@{}l}{\textbf{Consistency models}}\\\Xhline{3\arrayrulewidth}
        CD (LPIPS) & 1 & 3.55 \\
          & 2 & \textcolor{blue}{2.93} \\
        CT (LPIPS) & 1 & 8.70 \\
          & 2 & 5.83  \\
        iCT  & 1 & \textcolor{red}{2.83}  \\
        & 2 & \textcolor{blue}{2.46}  \\
        iCT-deep  & 1 & \textcolor{red}{2.51}  \\
        & 2 & \textcolor{blue}{\textbf{2.24}}  \\
        CTM  & 1 & 5.19 \\
        CTM  + GAN & 1 & \textcolor{red}{\textbf{1.98}}  \\
        \multicolumn{3}{@{}l}{\textbf{Rectified flows}}\\\Xhline{3\arrayrulewidth}
        1-rectified flow (+distill) 
         & 1 & 6.18 \\
        2-rectified flow  
         & 1 & 12.21 \\
         & 110 & 3.36  \\
        +distill 
         & 1 & 4.85 \\
        3-rectified flow    
         & 1 & 8.15 \\
         & 104 & 3.96  \\
        +Distill  
         & 1 & 5.21  \\
          
        
	\end{tabular}
    \end{adjustbox}
	}
\end{minipage}
\hfill
\begin{minipage}[t]{0.49\linewidth}
    \caption{Class-conditional generation on  CIFAR-10.}
    \label{tab:imagenet-64}
    \centering
    {\setlength{\extrarowheight}{0.4pt}
    \begin{adjustbox}{max width=\linewidth}
    \begin{tabular}{@{}l@{\hspace{0.2em}}c@{\hspace{0.3em}}c@{}}
        \Xhline{3\arrayrulewidth}
        METHOD & NFE ($\downarrow$) & FID ($\downarrow$) \\
        \\[-2ex]
        \multicolumn{1}{@{}l}{\textbf{Diffusion models}}\\\Xhline{3\arrayrulewidth}
        NCSN++-G & 2000 & 2.25 \\ 
        EDM
        & 35  & 1.79 \\
       
    \end{tabular}
    \end{adjustbox}
    }
\end{minipage}
% \captionsetup{labelformat=empty, labelsep=none, font=scriptsize}
\caption{The \textcolor{red}{red} rows correspond to the top-5 baselines for the 1-NFE setting, and the \textcolor{blue}{blue} rows correspond to the top 5 baselines for the 2-NFE setting. The lowest FID scores for 1-NFE and 2-NFE are \textbf{boldfaced}.}
% \vspace{-5mm}
\end{table*}
"""

EVALUATION = r"""
Frechet Inception Distance (FID) measure the quality of the generated images. The number of function evaluation (NFE) denotes the number of times we need to call the main neural network during inference. It coincides with the number of discretization steps N for ODE and SDE models.

The exact reference statistics when calculating FID for CIFAR-10 is in the directory `/workplace/dataset_candidate/cifar10-32x32.npz`, you can refer to it when you need to calculate the FID.
"""

REF = r"""
All this information is from EDM paper (Elucidating the Design Space of Diffusion-Based Generative Models), and the repository of EDM is in the directory `/workplace/dataset_candidate/edm`, you can refer to its README.md in `/workplace/dataset_candidate/edm/README.md` when you need to process the dataset or calculate the metrics.
"""