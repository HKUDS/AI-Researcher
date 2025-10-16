TASK = r"""
Train a GNN model for node classification on the given dataset.
"""


DATASET = r"""
The dataset for node classification is Cora, Citeseer, PubMed. 

You should the following code to load the dataset (detailed in the repository of GraphMAE in the directory `/workplace/dataset_candidate/GraphMAE`):

\begin{verbatim}
import torch
import torch.nn.functional as F

import torch_geometric.transforms as T
from torch_geometric.datasets import Planetoid, TUDataset
from torch_geometric.utils import add_self_loops, remove_self_loops, to_undirected, degree

from ogb.nodeproppred import PygNodePropPredDataset

from sklearn.preprocessing import StandardScaler
def load_dataset(dataset_name):
    if dataset_name == "ogbn-arxiv":
        dataset = PygNodePropPredDataset(name='ogbn-arxiv', root="./data")
        graph = dataset[0]
        num_nodes = graph.x.shape[0]
        graph.edge_index = to_undirected(graph.edge_index)
        graph.edge_index = remove_self_loops(graph.edge_index)[0]
        graph.edge_index = add_self_loops(graph.edge_index)[0]
        split_idx = dataset.get_idx_split()
        train_idx, val_idx, test_idx = split_idx["train"], split_idx["valid"], split_idx["test"]
        if not torch.is_tensor(train_idx):
            train_idx = torch.as_tensor(train_idx)
            val_idx = torch.as_tensor(val_idx)
            test_idx = torch.as_tensor(test_idx)
        train_mask = torch.full((num_nodes,), False).index_fill_(0, train_idx, True)
        val_mask = torch.full((num_nodes,), False).index_fill_(0, val_idx, True)
        test_mask = torch.full((num_nodes,), False).index_fill_(0, test_idx, True)
        graph.train_mask, graph.val_mask, graph.test_mask = train_mask, val_mask, test_mask
        graph.y = graph.y.view(-1)
        graph.x = scale_feats(graph.x)
    else:
        dataset = Planetoid("", dataset_name, transform=T.NormalizeFeatures())
        graph = dataset[0]
        graph.edge_index = remove_self_loops(graph.edge_index)[0]
        graph.edge_index = add_self_loops(graph.edge_index)[0]

    num_features = dataset.num_features
    num_classes = dataset.num_classes
    return graph, (num_features, num_classes)
\end{verbatim}
"""

BASELINE = r"""
SOTA contrastive self-supervised models
• Contrastive Self-supervised Models: DGI [7], MVGRL [1], GRACE [10], BGRL [6], InfoGCL [8], and CCA-SSG [9].
• Supervised Baselines: GCN and GAT.
• Generative Self-supervised Models: GAE [4], GPT-GNN [3], GATE [5] and GraphMAE [2].

References
[1] Kaveh Hassani and Amir Hosein Khasahmadi. Contrastive multi-view representation learning on graphs. In ICML, 2020.
[2] Zhenyu Hou, Xiao Liu, Yukuo Cen, Yuxiao Dong, Hongxia Yang, Chunjie Wang, and Jie Tang. Graphmae: Self-supervised masked graph autoencoders. In KDD, pages 594–604. ACM, 2022.
[3] Ziniu Hu, Yuxiao Dong, Kuansan Wang, Kai-Wei Chang, and Yizhou Sun. Gpt-gnn: Generative pre-training of graph neural networks. In SIGKDD, 2020.
[4] Thomas N Kipf and Max Welling. Variational graph auto-encoders. arXiv preprint arXiv:1611.07308, 2016.
[5] Amin Salehi and Hasan Davulcu. Graph attention auto-encoders. In ICTAI. IEEE, 2020.
[6] Shantanu Thakoor, Corentin Tallec, Mohammad Gheshlaghi Azar, R ́emi Munos, Petar Veliˇckovi ́c,
and Michal Valko. Large-scale representation learning on graphs via bootstrapping. In ICLR, 2022.
[7] Petar Veliˇckovi ́c, William Fedus, William L Hamilton, Pietro Li`o, Yoshua Bengio, and R Devon Hjelm. Deep graph infomax. In ICLR, 2018.
[8] Dongkuan Xu, Wei Cheng, Dongsheng Luo, Haifeng Chen, and Xiang Zhang. Infogcl: Information-aware graph contrastive learning. 2021.
[9] Hengrui Zhang, Qitian Wu, Junchi Yan, David Wipf, and Philip S Yu. From canonical correlation analysis to self-supervised graph neural networks. In NeurIPS, 2021.
[10] Yanqiao Zhu, Yichen Xu, Feng Yu, Qiang Liu, Shu Wu, and Liang Wang. Deep graph contrastive representation learning. arXiv preprint arXiv:2006.04131, 2020.
"""

COMPARISON = r"""
\begin{table*}[htbp]
    \centering
    \caption{Experiment results in unsupervised representation learning for \underline{node classification}. \textmd{We report the accuracy (\%) for all datasets. }
    }
    \begin{threeparttable}
    \renewcommand\tabcolsep{10pt}
    \renewcommand\arraystretch{1.05}
    \begin{tabular}{c|c|ccc}
        \toprule[1.2pt]
            & Dataset &   Cora      & CiteSeer      & PubMed               \\
        % \midrule
        % \multirow{3}{*}{Statistics}

         \midrule
        \multirow{2}{*}{Supervised} 
        & GCN     &  81.5          & 70.3          & 79.0                              \\
        & GAT     &  83.0$\pm$0.7  & 72.5$\pm$0.7  & 79.0$\pm$0.3                     \\
        \midrule
        \multirow{10}{*}{Self-supervised} 
        & GAE     &  71.5$\pm$0.4  & 65.8$\pm$0.4  & 72.1$\pm$0.5     \\
        & GPT-GNN &  80.1$\pm$1.0  & 68.4$\pm$1.6  & 76.3$\pm$0.8 \\
        & GATE    &  83.2$\pm$0.6  & 71.8$\pm$0.8  & 80.9$\pm$0.3            \\ 
        & DGI     &  82.3$\pm$0.6  & 71.8$\pm$0.7  & 76.8$\pm$0.6         \\
        & MVGRL   & 83.5$\pm$0.4   & 73.3$\pm$0.5  & 80.1$\pm$0.7        \\
        & GRACE$^{1}$   & 81.9$\pm$0.4   & 71.2$\pm$0.5  & 80.6$\pm$0.4           \\  
        & BGRL$^{1}$    & 82.7$\pm$0.6   & 71.1$\pm$0.8  & 79.6$\pm$0.5         \\
        & InfoGCL  & 83.5$\pm$0.3   & \bf 73.5$\pm$0.4  & 79.1$\pm$0.2  \\
        & CCA-SSG$^{1}$ & \underline{84.0$\pm$0.4}   & 73.1$\pm$0.3  & \underline{81.0$\pm$0.4}  \\
        % \cmidrule{2-4}
        %  & \model  & \bf 84.16±0.44  & \underline{73.35±0.42}  & \bf 81.10±0.41  & \bf 71.75$\pm$0.17 & \bf 74.50$\pm$0.29    & \bf 96.01$\pm$0.08    \\
         & GraphMAE  & \bf 84.2±0.4  & \underline{73.4±0.4}  & \bf 81.1±0.4   \\

        \bottomrule[1.2pt]
    \end{tabular}
     \begin{tablenotes}
        \footnotesize
        \item[] The results not reported are due to unavailable code or out-of-memory.
        \item[1] Results are from reproducing using authors' official code, as they did not report the results in part of datasets. The result of PPI is a bit different from what the authors' reported. This is because we train the linear classifier until convergence, rather than for a small fixed number of epochs during evaluation, using the official code.
    \end{tablenotes}

    \end{threeparttable}
    \label{tab:node_clf}
\end{table*}
"""

EVALUATION = r"""
For supervised settings, you should train the model with supervision on the training set and evaluate the trained mosdel on the test set.

For self-supervised settings, you should first train a GNN encoder by the model without supervision, and then freeze the parameters of the encoder and generate all the nodes' embeddings. 
For evaluation, you should train a linear classifier and report the mean accuracy on the test nodes through 20 random initializations. 

You should use the accuracy (\%) as metrics for all datasets.  
\begin{verbatim}
def accuracy(y_pred, y_true):
    y_true = y_true.squeeze().long()
    preds = y_pred.max(1)[1].type_as(y_true)
    correct = preds.eq(y_true).double()
    correct = correct.sum().item()
    return correct / len(y_true)
\end{verbatim}
"""

REF = r"""
All this information is from GraphMAE paper, and the repository of GraphMAE is in the directory `/workplace/dataset_candidate/GraphMAE`, you can refer to it when you need to process the dataset or calculate the metrics.
"""