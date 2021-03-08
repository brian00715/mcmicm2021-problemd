dataByArtistPath = 'E:\MCM&ICM2021\2021_MCM-ICM_Problems\2021_ICM_Problem_D_Data\data_by_artist.csv';
rawData = importdata(dataByArtistPath);
dataByArtist = rawData.data;
artistName = string(rawData.textdata(2:5855,1));
pureData = dataByArtist(1:5854,2:15);
[dataNum,dims] = size(pureData); % ����������ָ�����
stdMat=zscore(pureData); % ��׼��
corrMat = corrcoef(pureData);%�������ϵ������
[vecMat,eigenValue] = eig(corrMat);%���������������������ֵ

% �������ɷֹ����ʺ��ۼƹ�����
lambda = diag(eigenValue);  % diag�������ڵõ�һ����������Խ���Ԫ��ֵ(���ص���������)
lambda = lambda(end:-1:1);  % ��Ϊlambda�����Ǵ�С������ģ����ǽ������ͷ
contributionRate = lambda / sum(lambda);  % ������
sumContributionRate = cumsum(lambda)/ sum(lambda);   % �ۼƹ�����
vecMat=rot90(vecMat)';



pcaNum = 8; % ǰ8�����ɷֹ����ʴﵽ80%
dimReducedMat = zeros(dataNum,pcaNum);  %��ά��ľ���ÿһ����һ�����ɷ�
for i = 1:pcaNum
    veci = vecMat(:,i)';   % ����i����������ȡ������ת��Ϊ������
    veciRep = repmat(veci,dataNum,1);   % �ظ�dataNum�Σ���ԭ�������
    dimReducedMat(:, i) = sum(veciRep .* stdMat, 2);  % �Ա�׼������������Ȩ�غ�Ҫ����ÿһ�еĺ�
end

resultMat = [ artistName';dataByArtist(:,1)';dimReducedMat']';
resultMat = [string(rawData.textdata(1,1:10));resultMat];
writematrix(resultMat,'data_by_artist_dim_reduced.csv')
