dataByArtistPath = 'E:\MCM&ICM2021\2021_MCM-ICM_Problems\2021_ICM_Problem_D_Data\data_by_artist.csv';
rawData = importdata(dataByArtistPath);
dataByArtist = rawData.data;
artistName = string(rawData.textdata(2:5855,1));
pureData = dataByArtist(1:5854,2:15);
[dataNum,dims] = size(pureData); % 样本个数和指标个数
stdMat=zscore(pureData); % 标准化
corrMat = corrcoef(pureData);%计算相关系数矩阵
[vecMat,eigenValue] = eig(corrMat);%计算特征向量矩阵和特征值

% 计算主成分贡献率和累计贡献率
lambda = diag(eigenValue);  % diag函数用于得到一个矩阵的主对角线元素值(返回的是列向量)
lambda = lambda(end:-1:1);  % 因为lambda向量是从小大到排序的，我们将其调个头
contributionRate = lambda / sum(lambda);  % 贡献率
sumContributionRate = cumsum(lambda)/ sum(lambda);   % 累计贡献率
vecMat=rot90(vecMat)';



pcaNum = 8; % 前8个主成分贡献率达到80%
dimReducedMat = zeros(dataNum,pcaNum);  %降维后的矩阵，每一列是一个主成分
for i = 1:pcaNum
    veci = vecMat(:,i)';   % 将第i个特征向量取出，并转置为行向量
    veciRep = repmat(veci,dataNum,1);   % 重复dataNum次，与原矩阵对齐
    dimReducedMat(:, i) = sum(veciRep .* stdMat, 2);  % 对标准化的数据求了权重后要计算每一行的和
end

resultMat = [ artistName';dataByArtist(:,1)';dimReducedMat']';
resultMat = [string(rawData.textdata(1,1:10));resultMat];
writematrix(resultMat,'data_by_artist_dim_reduced.csv')
