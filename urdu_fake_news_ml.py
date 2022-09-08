# -*- coding: utf-8 -*-
"""urdu fake news ml.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lS4uKS528eUBnLz9HYqh0yBv5yS4y-Nd
"""

from google.colab import drive
drive.mount('/content/drive/')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My Drive/fake news

import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import StackingClassifier


from sklearn.metrics import confusion_matrix,matthews_corrcoef,classification_report
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np
df=pd.read_excel('news.xlsx')

labelencoder = LabelEncoder()
df['label'] = labelencoder.fit_transform(df['label'])
#df.head()
X=df.drop(['label'],axis=1)

y=df['label']

verbs = open("urduverbswithforms.txt",encoding='utf-8').read().split()

import re
corpus = [] 
for i in range(0, len(df)):
    review = re.sub('[^آ-ے]', ' ', str(df['news'][i]))
    review = review.split()
    #print(review)
    #review = [word for word in review if not word in stop_words]
    #review = [word for word in review if not word in verbs]
    
    review = [word for word in review if word in verbs]
    #review2 = [word for word in review if not verbs in verbs]

    #list3 = set(review1)&set(review2)
    #list4 = sorted(list3, key = lambda k : review1.index(k))

    #print(review) 
    review = ' '.join(review)
    corpus.append(review)

import re
corpus1 = [] 
for i in range(0, len(df)):
    review = re.sub('[^آ-ے]', ' ', str(df['news'][i]))
    review = review.split()
    #print(review)
    #review = [word for word in review if not word in stop_words]
    #review = [word for word in review if not word in verbs]
    
    #review = [word for word in review if word in verbs]
    #review2 = [word for word in review if not verbs in verbs]

    #list3 = set(review1)&set(review2)
    #list4 = sorted(list3, key = lambda k : review1.index(k))

    #print(review) 
    review = ' '.join(review)
    corpus1.append(review)

"""# Feature Extraction"""

ng=(1,1)
w='word'
c='char'
from sklearn.feature_extraction.text import TfidfVectorizer as tfidf
from sklearn.feature_extraction.text import CountVectorizer
tfidf_v=tfidf(max_features=None,analyzer=w,ngram_range=ng)
tfidf_v1=tfidf(max_features=None,analyzer=w,ngram_range=ng)

X=tfidf_v.fit_transform(corpus).toarray()
X1=tfidf_v1.fit_transform(corpus1).toarray()

X3=np.hstack((X,X1))

X_train, X_test, y_train, y_test = train_test_split(X3, y, test_size=0.3,stratify=y,random_state=42)

clfs = list()
clfs.append(('rf',RandomForestClassifier()))
clfs.append(('extra',ExtraTreesClassifier()))
clfs_est = LogisticRegression()
stack = StackingClassifier(estimators=clfs, final_estimator=clfs_est)

bnb=stack.fit(X_train,y_train)
bnb_p=bnb.predict(X_test)

lr=LogisticRegression().fit(X_train,y_train)
et=ExtraTreesClassifier().fit(X_train,y_train)
rf=RandomForestClassifier().fit(X_train,y_train)
knn=KNeighborsClassifier().fit(X_train,y_train)
svc=SVC(probability=True).fit(X_train,y_train)

from sklearn.metrics import roc_curve, roc_auc_score

rf_probs = rf.predict_proba(X_test)
rf_probs = rf_probs[:, 1]
rf_auc = roc_auc_score(y_test, rf_probs)
rf_fpr, rf_tpr, threshold = roc_curve(y_test, rf_probs)

lr_probs = lr.predict_proba(X_test)
lr_probs = lr_probs[:, 1]
lr_auc = roc_auc_score(y_test, lr_probs)
lr_fpr, lr_tpr, threshold = roc_curve(y_test, lr_probs)

ber_probs = bnb.predict_proba(X_test)
ber_probs = ber_probs[:, 1]
ber_auc = roc_auc_score(y_test, ber_probs)
stack_fpr, stack_tpr, thresholdb = roc_curve(y_test, ber_probs)

et_probs = et.predict_proba(X_test)
et_probs = et_probs[:, 1]
et_auc = roc_auc_score(y_test, et_probs)
et_fpr, et_tpr, thresholde = roc_curve(y_test, et_probs)


knn_probs = knn.predict_proba(X_test)
knn_probs = knn_probs[:, 1]
knn_auc = roc_auc_score(y_test, knn_probs)
knn_fpr, knn_tpr, thresholde = roc_curve(y_test, knn_probs)

svc_probs = svc.predict_proba(X_test)
svc_probs = svc_probs[:, 1]
svc_auc = roc_auc_score(y_test, svc_probs)
svc_fpr, svc_tpr, thresholde = roc_curve(y_test, svc_probs)

plt.figure(figsize=(10, 5), dpi=300)
plt.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)
plt.plot(et_fpr, et_tpr, marker='.', label='Extra Trees (auc = %0.3f)' % et_auc)
plt.plot(svc_fpr, svc_tpr, marker='.', label='Support Vector (auc = %0.3f)' % svc_auc)
plt.plot(knn_fpr, knn_tpr, marker='.', label='K-Nearest (auc = %0.3f)' % knn_auc)
plt.plot(stack_fpr, stack_tpr, marker='.', label='Stacking (ET,RF) (auc = %0.3f)' % ber_auc)
plt.plot(rf_fpr, rf_tpr, linestyle='-', label='Random Forest (auc = %0.3f)' % rf_auc)



plt.xlabel('False Positive Rate -->')
plt.ylabel('True Positive Rate -->')

plt.legend(loc="lower right", fontsize=15, ncol=1)

plt.show()





cm1 = confusion_matrix(y_test,bnb_p)
print('Confusion Matrix : \n', cm1)

array4=[[688,  39],
 [44, 459]]
import matplotlib.pyplot as plt
import seaborn as sns
RF = pd.DataFrame(array4, index = [i for i in "10"],
                  columns = [i for i in "10"])

i=1
def plot_sub_sentiment(Airline):
    sns.set()
    #tmp = rfc.fit(X_train, y_train.ravel())
    sns.heatmap(Airline,annot=True,fmt = "d",linecolor="k",linewidths=3)
    plt.title("",fontsize=8)

plt.figure(1,figsize=(4, 4),dpi=500)
plt.subplot(111) 
plot_sub_sentiment(RF)


plt.tight_layout(pad=0) 
plt.title("10 CV testing for stacked approach using BOW")
# Show graphic
plt.savefig('ConGBM.pdf')
plt.show()

from sklearn.metrics import f1_score

cm1 = confusion_matrix(y_test,bnb_p)
tp=cm1[0,0]
fp=cm1[0,1]
fn=cm1[1,0]
tn=cm1[1,1]

pr=tp/(tp+fp)
rc=tp/(tp+fn)
#f1=2*(pr*rc)/(pr+rc)
print("Accuracy",metrics.accuracy_score(y_test,bnb_p)*100)
print("Precision", pr*100)
print("Sen", rc*100)
print("F1",f1_score(y_test, bnb_p, average='macro')*100)

#print(classification_report(y_test,bnb_p))

#Confusion matrix, Accuracy, sensitivity and specificity
from sklearn.metrics import confusion_matrix,matthews_corrcoef,classification_report
#st=stack.fit(X_train,y_train)
#st_pred=st.predict(X_test)

cm1 = confusion_matrix(y_test,bnb_p)
print('Confusion Matrix : \n', cm1)

total1=sum(sum(cm1))
#####from confusion matrix calculate accuracy
accuracy1=(cm1[0,0]+cm1[1,1])/total1
print ('Accuracy : ', accuracy1)

sensitivity1 = cm1[0,0]/(cm1[0,0]+cm1[0,1])
print('Sensitivity : ', sensitivity1 )

specificity1 = cm1[1,1]/(cm1[1,0]+cm1[1,1])
print('Specificity : ', specificity1)
print("MCC RF: ",matthews_corrcoef(y_test,bnb_p)*100)
#print(classification_report(y_test,bnb_p))

from sklearn.metrics import f1_score

cm2 = confusion_matrix(y_test,ber_p)
tp=cm2[0,0]
fp=cm2[0,1]
fn=cm2[1,0]
tn=cm2[1,1]

pr1=tp/(tp+fp)
rc1=tp/(tp+fn)
#f1=2*(pr*rc)/(pr+rc)
print("Accuracy",metrics.accuracy_score(y_test,ber_p)*100)
print("Precision", pr*100)
print("Recall", rc*100)
print("F1",f1_score(y_test, ber_p, average='macro')*100)

#print(classification_report(y_test,bnb_p))

from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import confusion_matrix,matthews_corrcoef,classification_report
from sklearn import metrics
et=ExtraTreesClassifier().fit(X_train,y_train)
et_p=et.predict(X_test)

from sklearn.metrics import roc_curve, roc_auc_score

rf_probs = bnb.predict_proba(X_test)
rf_probs = rf_probs[:, 1]
rf_auc = roc_auc_score(y_test, rf_probs)
rf_fpr, rf_tpr, threshold = roc_curve(y_test, rf_probs)

ber_probs = ber.predict_proba(X_test)
ber_probs = ber_probs[:, 1]
ber_auc = roc_auc_score(y_test, ber_probs)
rf_fprb, rf_tprb, thresholdb = roc_curve(y_test, ber_probs)

et_probs = et.predict_proba(X_test)
et_probs = et_probs[:, 1]
et_auc = roc_auc_score(y_test, et_probs)
rf_fpre, rf_tpre, thresholde = roc_curve(y_test, et_probs)


plt.figure(figsize=(10, 5), dpi=300)
plt.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)
plt.plot(rf_fpre, rf_tpre, marker='.', label='Extra Trees (auc = %0.3f)' % et_auc)
plt.plot(rf_fprb, rf_tprb, marker='.', label='Bernoulli NB (auc = %0.3f)' % ber_auc)
plt.plot(rf_fpr, rf_tpr, linestyle='-', label='Stacking (auc = %0.3f)' % rf_auc)



plt.xlabel('False Positive Rate -->')
plt.ylabel('True Positive Rate -->')

plt.legend(loc="lower right", fontsize=15, ncol=1)

plt.show()



from sklearn.metrics import accuracy_score,confusion_matrix,matthews_corrcoef
from sklearn.model_selection import StratifiedKFold

mcc=[]
sp=[]
sn=[]
f1=[]
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=1)
lst_accu_stratified = []
for train_index, test_index in skf.split(X3, y):
    x_train_fold, x_test_fold = X3[train_index], X3[test_index]
    y_train_fold, y_test_fold = y[train_index], y[test_index]
    #print(y_train_fold)
    knn.fit(x_train_fold, y_train_fold)
    lst_accu_stratified.append(knn.score(x_test_fold, y_test_fold))

    pred_lr5=knn.predict(x_test_fold)
    cm1 = confusion_matrix(y_test_fold,pred_lr5)
    total1=sum(sum(cm1))
    accuracy1=(cm1[0,0]+cm1[1,1])/total1

    sensitivity1 = cm1[0,0]/(cm1[0,0]+cm1[0,1])
    sn.append(sensitivity1)

    specificity1 = cm1[1,1]/(cm1[1,0]+cm1[1,1])
    sp.append(specificity1)
    mccc=matthews_corrcoef(pred_lr5, y_test_fold)
    mcc.append(mccc)
    f1=f1_score(y_test_fold, pred_lr5, average='macro')
    print(f1)
    #f1.append(f1)
    #cmlr = confusion_matrix(x_test_fold,y_test_fold)
#print('Confusion Matrix : \n', cmlr)
import numpy as np
print('\n Accuracy:',np.mean(lst_accu_stratified)*100)
#print('\n SP:',np.mean(sp)*100)
#print('\nSN:',np.mean(sn)*100)
#print('\n MCC:',np.mean(mcc)*100)
#print('\n F1:',np.mean(f1)*100)

from sklearn.metrics import RocCurveDisplay
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC 
from sklearn.linear_model import RidgeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import auc
# Add noisy features
random_state = np.random.RandomState(0)
#cv = StratifiedKFold(n_splits=5)
#classifier = SVC(kernel="linear", probability=True, random_state=random_state)
#classifier=LogisticRegression()
classifier=stack

tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 100)

fig, ax = plt.subplots()
for i, (train, test) in enumerate(cv.split(X, y)):
    classifier.fit(X[train], y[train])
    viz = RocCurveDisplay.from_estimator(
        classifier,
        X[test],
        y[test],
        name="ROC fold {}".format(i),
        alpha=0.3,
        lw=1,
        ax=ax,
    )
    interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
    interp_tpr[0] = 0.0
    tprs.append(interp_tpr)
    aucs.append(viz.roc_auc)

ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)

mean_tpr = np.mean(tprs, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs)
ax.plot(
    mean_fpr,
    mean_tpr,
    color="b",
    label=r"Mean ROC (AUC = %0.3f $\pm$ %0.3f)" % (mean_auc, std_auc),
    lw=2,
    alpha=0.8,
)

std_tpr = np.std(tprs, axis=0)
tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
ax.fill_between(
    mean_fpr,
    tprs_lower,
    tprs_upper,
    color="grey",
    alpha=0.2,
    label=r"$\pm$ 1 std. dev.",
)

ax.set(
    xlim=[-0.05, 1.05],
    ylim=[-0.05, 1.05],
    title="Receiver operating characteristic Stack",
)
ax.legend(loc="lower right")
plt.show()
viz_fpr=viz.fpr
viz_tpr=viz.tpr
mean_auc
#stack

from sklearn.metrics import RocCurveDisplay
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC 
from sklearn.linear_model import RidgeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import auc
# Add noisy features
random_state = np.random.RandomState(0)
#cv = StratifiedKFold(n_splits=10)
#classifier = SVC(kernel="linear", probability=True, random_state=random_state)
#classifier=LogisticRegression()
classifier_rf=RandomForestClassifier()

tprs_rf = []
aucs_rf = []
mean_fpr_rf = np.linspace(0, 1, 100)

fig, ax = plt.subplots()
for i, (train, test) in enumerate(cv.split(X, y)):
    classifier_rf.fit(X[train], y[train])
    viz_rf = RocCurveDisplay.from_estimator(
        classifier_rf,
        X[test],
        y[test],
        name="ROC fold {}".format(i),
        alpha=0.3,
        lw=1,
        ax=ax,
    )
    interp_tpr_rf = np.interp(mean_fpr_rf, viz_rf.fpr, viz_rf.tpr)
    interp_tpr[0] = 0.0
    tprs_rf.append(interp_tpr_rf)
    aucs_rf.append(viz_rf.roc_auc)

ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)

mean_tpr_rf = np.mean(tprs_rf, axis=0)
mean_tpr_rf[-1] = 1.0
mean_auc_rf = auc(mean_fpr_rf, mean_tpr_rf)
std_auc_rf = np.std(aucs)
ax.plot(
    mean_fpr_rf,
    mean_tpr_rf,
    color="b",
    label=r"Mean ROC (AUC = %0.3f $\pm$ %0.3f)" % (mean_auc_rf, std_auc_rf),
    lw=2,
    alpha=0.8,
)

std_tpr_rf = np.std(tprs_rf, axis=0)
tprs_upper_rf = np.minimum(mean_tpr_rf + std_tpr_rf, 1)
tprs_lower_rf = np.maximum(mean_tpr_rf - std_tpr_rf, 0)
ax.fill_between(
    mean_fpr_rf,
    tprs_lower_rf,
    tprs_upper_rf,
    color="grey",
    alpha=0.2,
    label=r"$\pm$ 1 std. dev.",
)

ax.set(
    xlim=[-0.05, 1.05],
    ylim=[-0.05, 1.05],
    title="Receiver operating characteristic Random Forest",
)
ax.legend(loc="lower right")
plt.show()
viz_fpr_rf=viz_rf.fpr
viz_tpr_rf=viz_rf.tpr
mean_auc_rf

from sklearn.metrics import RocCurveDisplay
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC 
from sklearn.linear_model import RidgeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import auc
# Add noisy features
random_state = np.random.RandomState(0)
#cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
#classifier = SVC(kernel="linear", probability=True, random_state=random_state)
#classifier=LogisticRegression()
classifier_lr= LogisticRegression()

tprs_lr = []
aucs_lr = []
mean_fpr_lr = np.linspace(0, 1, 100)

fig, ax = plt.subplots()
for i, (train, test) in enumerate(cv.split(X, y)):
    classifier_lr.fit(X[train], y[train])
    viz_lr = RocCurveDisplay.from_estimator(
        classifier_lr,
        X[test],
        y[test],
        name="ROC fold {}".format(i),
        alpha=0.3,
        lw=1,
        ax=ax,
    )
    interp_tpr_lr = np.interp(mean_fpr_lr, viz_lr.fpr, viz_lr.tpr)
    interp_tpr[0] = 0.0
    tprs_lr.append(interp_tpr_lr)
    aucs_lr.append(viz_lr.roc_auc)

ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)

mean_tpr_lr = np.mean(tprs_lr, axis=0)
mean_tpr_lr[-1] = 1.0
mean_auc_lr = auc(mean_fpr_lr, mean_tpr_lr)
std_auc_lr = np.std(aucs)
ax.plot(
    mean_fpr_lr,
    mean_tpr_lr,
    color="b",
    label=r"Mean ROC (AUC = %0.3f $\pm$ %0.3f)" % (mean_auc_lr, std_auc_lr),
    lw=2,
    alpha=0.8,
)

std_tpr_lr = np.std(tprs_lr, axis=0)
tprs_upper_lr = np.minimum(mean_tpr_lr + std_tpr_lr, 1)
tprs_lower_lr = np.maximum(mean_tpr_lr - std_tpr_lr, 0)
ax.fill_between(
    mean_fpr_lr,
    tprs_lower_lr,
    tprs_upper_lr,
    color="grey",
    alpha=0.2,
    label=r"$\pm$ 1 std. dev.",
)

ax.set(
    xlim=[-0.05, 1.05],
    ylim=[-0.05, 1.05],
    title="Receiver operating characteristic Logistic Regression",
)
ax.legend(loc="lower right")
plt.show()
viz_fpr_lr=viz_lr.fpr
viz_tpr_lr=viz_lr.tpr
mean_auc_lr

from sklearn.metrics import RocCurveDisplay
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC 
from sklearn.linear_model import RidgeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import auc
# Add noisy features
random_state = np.random.RandomState(0)
#cv = StratifiedKFold(n_splits=10)
#classifier = SVC(kernel="linear", probability=True, random_state=random_state)
#classifier=LogisticRegression()
classifier_et= ExtraTreesClassifier()

tprs_et = []
aucs_et = []
mean_fpr_et = np.linspace(0, 1, 100)

fig, ax = plt.subplots()
for i, (train, test) in enumerate(cv.split(X, y)):
    classifier_et.fit(X[train], y[train])
    viz_et = RocCurveDisplay.from_estimator(
        classifier_et,
        X[test],
        y[test],
        name="ROC fold {}".format(i),
        alpha=0.3,
        lw=1,
        ax=ax,
    )
    interp_tpr_et = np.interp(mean_fpr_et, viz_et.fpr, viz_et.tpr)
    interp_tpr[0] = 0.0
    tprs_et.append(interp_tpr_et)
    aucs_et.append(viz_et.roc_auc)

ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)

mean_tpr_et = np.mean(tprs_et, axis=0)
mean_tpr_et[-1] = 1.0
mean_auc_et = auc(mean_fpr_et, mean_tpr_et)
std_auc_et = np.std(aucs)
ax.plot(
    mean_fpr_et,
    mean_tpr_et,
    color="b",
    label=r"Mean ROC (AUC = %0.3f $\pm$ %0.3f)" % (mean_auc_et, std_auc_et),
    lw=2,
    alpha=0.8,
)

std_tpr_et = np.std(tprs_et, axis=0)
tprs_upper_et = np.minimum(mean_tpr_et + std_tpr_et, 1)
tprs_lower_et = np.maximum(mean_tpr_et - std_tpr_et, 0)
ax.fill_between(
    mean_fpr_et,
    tprs_lower_et,
    tprs_upper_et,
    color="grey",
    alpha=0.2,
    label=r"$\pm$ 1 std. dev.",
)

ax.set(
    xlim=[-0.05, 1.05],
    ylim=[-0.05, 1.05],
    title="Receiver operating characteristic Random Forest",
)
ax.legend(loc="lower right")
plt.show()
viz_fpr_et=viz_et.fpr
viz_tpr_et=viz_et.tpr
mean_auc_et

from sklearn.metrics import RocCurveDisplay
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC 
from sklearn.linear_model import RidgeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import auc
# Add noisy features
random_state = np.random.RandomState(0)
#cv = StratifiedKFold(n_splits=10)
#classifier = SVC(kernel="linear", probability=True, random_state=random_state)
#classifier=LogisticRegression()
classifier_svc= svc5

tprs_svc = []
aucs_svc = []
mean_fpr_svc = np.linspace(0, 1, 100)

fig, ax = plt.subplots()
for i, (train, test) in enumerate(cv.split(X, y)):
    classifier_svc.fit(X[train], y[train])
    viz_svc = RocCurveDisplay.from_estimator(
        classifier_svc,
        X[test],
        y[test],
        name="ROC fold {}".format(i),
        alpha=0.3,
        lw=1,
        ax=ax,
    )
    interp_tpr_svc = np.interp(mean_fpr_svc, viz_svc.fpr, viz_svc.tpr)
    interp_tpr[0] = 0.0
    tprs_svc.append(interp_tpr_svc)
    aucs_svc.append(viz_svc.roc_auc)

ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)

mean_tpr_svc = np.mean(tprs_svc, axis=0)
mean_tpr_svc[-1] = 1.0
mean_auc_svc = auc(mean_fpr_svc, mean_tpr_svc)
std_auc_svc = np.std(aucs)
ax.plot(
    mean_fpr_svc,
    mean_tpr_svc,
    color="b",
    label=r"Mean ROC (AUC = %0.3f $\pm$ %0.3f)" % (mean_auc_svc, std_auc_svc),
    lw=2,
    alpha=0.8,
)

std_tpr_svc = np.std(tprs_svc, axis=0)
tprs_upper_svc = np.minimum(mean_tpr_svc + std_tpr_svc, 1)
tprs_lower_svc = np.maximum(mean_tpr_svc - std_tpr_svc, 0)
ax.fill_between(
    mean_fpr_svc,
    tprs_lower_svc,
    tprs_upper_svc,
    color="grey",
    alpha=0.2,
    label=r"$\pm$ 1 std. dev.",
)

ax.set(
    xlim=[-0.05, 1.05],
    ylim=[-0.05, 1.05],
    title="Receiver operating characteristic Random Forest",
)
ax.legend(loc="lower right")
plt.show()
viz_fpr_svc=viz_svc.fpr
viz_tpr_svc=viz_svc.tpr
mean_auc_svc

from sklearn.metrics import RocCurveDisplay
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC 
from sklearn.linear_model import RidgeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import auc
# Add noisy features
random_state = np.random.RandomState(0)
#cv = StratifiedKFold(n_splits=10)
#classifier = SVC(kernel="linear", probability=True, random_state=random_state)
#classifier=LogisticRegression()
classifier_knn= knn5

tprs_knn = []
aucs_knn = []
mean_fpr_knn = np.linspace(0, 1, 100)

fig, ax = plt.subplots()
for i, (train, test) in enumerate(cv.split(X, y)):
    classifier_knn.fit(X[train], y[train])
    viz_knn = RocCurveDisplay.from_estimator(
        classifier_knn,
        X[test],
        y[test],
        name="ROC fold {}".format(i),
        alpha=0.3,
        lw=1,
        ax=ax,
    )
    interp_tpr_knn = np.interp(mean_fpr_knn, viz_knn.fpr, viz_knn.tpr)
    interp_tpr[0] = 0.0
    tprs_knn.append(interp_tpr_knn)
    aucs_knn.append(viz_knn.roc_auc)

ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Chance", alpha=0.8)

mean_tpr_knn = np.mean(tprs_knn, axis=0)
mean_tpr_knn[-1] = 1.0
mean_auc_knn = auc(mean_fpr_knn, mean_tpr_knn)
std_auc_knn = np.std(aucs)
ax.plot(
    mean_fpr_knn,
    mean_tpr_knn,
    color="b",
    label=r"Mean ROC (AUC = %0.3f $\pm$ %0.3f)" % (mean_auc_knn, std_auc_knn),
    lw=2,
    alpha=0.8,
)

std_tpr_knn = np.std(tprs_knn, axis=0)
tprs_upper_knn = np.minimum(mean_tpr_knn + std_tpr_knn, 1)
tprs_lower_knn = np.maximum(mean_tpr_knn - std_tpr_knn, 0)
ax.fill_between(
    mean_fpr_knn,
    tprs_lower_knn,
    tprs_upper_knn,
    color="grey",
    alpha=0.2,
    label=r"$\pm$ 1 std. dev.",
)

ax.set(
    xlim=[-0.05, 1.05],
    ylim=[-0.05, 1.05],
    title="Receiver operating characteristic Random Forest",
)
ax.legend(loc="lower right")
plt.show()
viz_fpr_knn=viz_knn.fpr
viz_tpr_knn=viz_knn.tpr
mean_auc_knn



plt.figure(figsize=(5, 5), dpi=600)
plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--",label= 'Chance (auc = %0.3f)'% 0.5)
plt.plot(viz_fpr_et, viz_tpr_et, linestyle='-', label='Extra Trees (auc = %0.3f)' % mean_auc_et)
plt.plot(viz_fpr_lr, viz_tpr_lr, marker='.', label='Logistic Regression (auc = %0.3f)' % mean_auc_lr)
plt.plot(viz_fpr_rf, viz_tpr_rf, marker='.', label='Random Forest (auc = %0.3f)' % mean_auc_rf)
plt.plot(viz_fpr, viz_tpr, marker='.', label='Stacked (ET,RF) (auc = %0.3f)' % mean_auc)
plt.plot(viz_fpr_svc, viz_tpr_svc, marker='.', label='Support Vector (auc = %0.3f)' % mean_auc_svc)
plt.plot(viz_fpr_knn, viz_tpr_knn, marker='.', label='K Nearest (auc = %0.3f)' % mean_auc_knn)

plt.title("5 Fold Mean Roc-auc")
plt.xlabel('False Positive Rate -->')
plt.ylabel('True Positive Rate -->')

plt.legend(loc="lower right", fontsize=9, ncol=1)

plt.show()

viz_fpr_et=viz_et.fpr
viz_tpr_et=viz_et.tpr
mean_auc_et

viz_fpr=viz.fpr
viz_tpr=viz.tpr
mean_auc

#Confusion matrix, Accuracy, sensitivity and specificity
from sklearn.metrics import confusion_matrix,matthews_corrcoef

cm1 = confusion_matrix(y,re)
print('Confusion Matrix : \n', cm1)

total1=sum(sum(cm1))
#####from confusion matrix calculate accuracy
accuracy1=(cm1[0,0]+cm1[1,1])/total1
print ('Accuracy : ', accuracy1)

sensitivity1 = cm1[0,0]/(cm1[0,0]+cm1[0,1])
print('Sensitivity : ', sensitivity1 )

specificity1 = cm1[1,1]/(cm1[1,0]+cm1[1,1])
print('Specificity : ', specificity1)
print("MCC RF: ",matthews_corrcoef(y,re)*100)

"""### 10 RF"""

from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=1)
lst_accu_stratified = []
for train_index, test_index in skf.split(x_scaled, y):
    x_train_fold, x_test_fold = x_scaled[train_index], x_scaled[test_index]
    y_train_fold, y_test_fold = y[train_index], y[test_index]
    #print(y_train_fold)
    rfcv5.fit(x_train_fold, y_train_fold)
    lst_accu_stratified.append(rfcv5.score(x_test_fold, y_test_fold))
    #cmlr = confusion_matrix(x_test_fold,y_test_fold)
#print('Confusion Matrix : \n', cmlr)
import numpy as np
print('List of possible accuracy:', lst_accu_stratified)
print('\nMaximum Accuracy :',max(lst_accu_stratified)*100, '%')
print('\nMinimum Accuracy:',min(lst_accu_stratified)*100)
print('\nOverall Accuracy:',np.mean(lst_accu_stratified)*100)

from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=1)
lst_accu_stratified = []
for train_index, test_index in skf.split(X, y):
    x_train_fold, x_test_fold = x_scaled[train_index], x_scaled[test_index]
    y_train_fold, y_test_fold = y[train_index], y[test_index]
    #print(y_train_fold)
    etcv5.fit(x_train_fold, y_train_fold)
    lst_accu_stratified.append(etcv5.score(x_test_fold, y_test_fold))
    #cmlr = confusion_matrix(x_test_fold,y_test_fold)
#print('Confusion Matrix : \n', cmlr)
import numpy as np
#print('List of possible accuracy:', lst_accu_stratified)
print('\nMaximum Accuracy :',max(lst_accu_stratified)*100, '%')
print('\nMinimum Accuracy:',min(lst_accu_stratified)*100)
print('\nOverall Accuracy:',np.mean(lst_accu_stratified)*100)

x_scaled

from sklearn.preprocessing import StandardScaler

#from lightgbm import LGBMClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
#lgbm=LGBMClassifier().fit(X_train,y_train)
rf=RandomForestClassifier().fit(X_train,y_train)
#lr=LogisticRegression().fit(X,y)
#xtre=ExtraTreesClassifier().fit(X_train,y_train)

from sklearn import metrics

pred_lr = rf.predict(X_test)
metrics.accuracy_score(y_test,pred_lr)*100

#pred_xtre = xtre.predict(X_test)
#metrics.accuracy_score(y_test,pred_xtre)*100


#pred_rf = rf.predict(X_test)
#metrics.accuracy_score(y_test,pred_rf)*100



#Confusion matrix, Accuracy, sensitivity and specificity
from sklearn.metrics import confusion_matrix,matthews_corrcoef

cm1 = confusion_matrix(y,pred_lr)
print('Confusion Matrix : \n', cm1)

total1=sum(sum(cm1))
#####from confusion matrix calculate accuracy
accuracy1=(cm1[0,0]+cm1[1,1])/total1
print ('Accuracy : ', accuracy1)

sensitivity1 = cm1[0,0]/(cm1[0,0]+cm1[0,1])
print('Sensitivity : ', sensitivity1 )

specificity1 = cm1[1,1]/(cm1[1,0]+cm1[1,1])
print('Specificity : ', specificity1)
print("MCC RF: ",matthews_corrcoef(y,pred_lr)*100)



from sklearn.metrics import roc_curve, auc,roc_auc_score

rf_probs = rf.predict_proba(X_test)
rf_probs = rf_probs[:, 1]
rf_auc = roc_auc_score(y_test, rf_probs)
rf_fpr, rf_tpr, threshold = roc_curve(y_test, rf_probs)

lr_probs = lr.predict_proba(X_test)
lr_probs = lr_probs[:, 1]
lr_auc = roc_auc_score(y_test, lr_probs)
lr_fpr, lr_tpr, threshold = roc_curve(y_test, lr_probs)


xtre_probs = xtre.predict_proba(X_test)
xtre_probs = xtre_probs[:, 1]
xtre_auc = roc_auc_score(y_test, xtre_probs)
xtre_fpr, xtre_tpr, threshold = roc_curve(y_test, xtre_probs)



st_probs = stack.predict_proba(X_test)
st_probs = st_probs[:, 1]
st_auc = roc_auc_score(y_test, st_probs)
st_fpr, st_tpr, threshold = roc_curve(y_test, st_probs)

plt.figure(figsize=(5, 5), dpi=600)
plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--",label= 'Chance (auc = %0.3f)'% 0.5)
#plt.plot(ridge_fpr, ridge_tpr, linestyle='-', label='SVM (auc = %0.3f)' % ridge_auc)
plt.plot(rf_fpr, rf_tpr, marker='.', label='Random Forest (auc = %0.3f)' % rf_auc)
plt.plot(lr_fpr, lr_tpr, marker='.', label='Logistic Regression (auc = %0.3f)' % lr_auc)
plt.plot(xtre_fpr, xtre_tpr, marker='.', label='Extra Trees (auc = %0.3f)' % xtre_auc)
plt.plot(st_fpr, st_tpr, marker='.', label='Stacked (auc = %0.3f)' % st_auc)


plt.xlabel('False Positive Rate -->')
plt.ylabel('True Positive Rate -->')

plt.legend(loc="lower right", fontsize=9, ncol=1)

plt.show()



from sklearn.ensemble import StackingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
clfs = list()
#clfs.append(('ridge', ridge))
clfs.append(('rf',RandomForestClassifier()))
clfs.append(('extra',ExtraTreesClassifier()))
#clfs.append(('lgbm',lgbm))
clfs_est = LogisticRegression()
stack = StackingClassifier(estimators=clfs, final_estimator=clfs_est)
stack=stack.fit(X_train, y_train)
#pred_model = stack.predict(X_test)
#acc_test_model= metrics.accuracy_score(y_test,pred_model)*100
#print('Test accuracy  ',acc_test_model)

pred_model = stack.predict(X_test)
acc_test_model_stack1= metrics.accuracy_score(y_test,pred_model)*100
print('Test accuracy  ',acc_test_model_stack1)

#Confusion matrix, Accuracy, sensitivity and specificity
from sklearn.metrics import confusion_matrix,matthews_corrcoef

cm1 = confusion_matrix(y_test,pred_model)
print('Confusion Matrix : \n', cm1)

total1=sum(sum(cm1))
#####from confusion matrix calculate accuracy
accuracy1=(cm1[0,0]+cm1[1,1])/total1
print ('Accuracy : ', accuracy1)

sensitivity1 = cm1[0,0]/(cm1[0,0]+cm1[0,1])
print('Sensitivity : ', sensitivity1 )

specificity1 = cm1[1,1]/(cm1[1,0]+cm1[1,1])
print('Specificity : ', specificity1)
print("MCC RF: ",matthews_corrcoef(y_test,pred_model)*100)

from sklearn.ensemble import StackingClassifier
from sklearn import metrics
clfs1 = list()
#clfs.append(('ridge', ridge))
clfs1.append(('rf',rf))
#clfs.append(('extra',xtre))
#clfs.append(('lgbm',lgbm))
clfs_est1 = xtre
stack1 = StackingClassifier(estimators=clfs1, final_estimator=clfs_est1, cv=5)
stack1=stack1.fit(X_train, y_train)
#pred_model = stack.predict(X_test)
#acc_test_model= metrics.accuracy_score(y_test,pred_model)*100
#print('Test accuracy  ',acc_test_model)

pred_model1 = stack1.predict(X_test)
acc_test_model2= metrics.accuracy_score(y_test,pred_model1)*100
print('Test accuracy  ',acc_test_model2)

from sklearn.ensemble import StackingClassifier
from sklearn import metrics
clfs2 = list()
clfs2.append(('stack', stack))
clfs2.append(('stack1',stack1))
#clfs.append(('extra',xtre))
#clfs.append(('lgbm',lgbm))
stackad = StackingClassifier(estimators=clfs2, cv=5)
stackad=stackad.fit(X_train, y_train)
#pred_model = stack.predict(X_test)

pred_model2st = stackad.predict(X_test)
acc_test_model= metrics.accuracy_score(y_test,pred_model2st)*100
print('Test accuracy  ',acc_test_model)



from sklearn.metrics import plot_confusion_matrix
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

plot_confusion_matrix(stack, X_test, y_test)  
plt.show()

from sklearn.metrics import matthews_corrcoef
print("MCC STack: ",matthews_corrcoef(y_test,pred_model)*100)



#predicting probabilities
from sklearn.metrics import roc_curve, roc_auc_score

rf_probs = rf.predict_proba(X_test)
lr_probs = lr.predict_proba(X_test)
#lgbm_probs = lgbm.predict_proba(X_test)
xtre_probs = xtre.predict_proba(X_test)
stack_probs = stack.predict_proba(X_test)

rf_probs = rf_probs[:, 1]
lr_probs = lr_probs[:, 1]
#lgbm_probs = lgbm_probs[:, 1]
xtre_probs = xtre_probs[:, 1]
stack_probs = stack_probs[:, 1]


#calclulate the rocauc score
rf_auc = roc_auc_score(y_test, rf_probs)
lr_auc = roc_auc_score(y_test, lr_probs)
#lgbm_auc = roc_auc_score(y_test, lgbm_probs)
xtre_auc = roc_auc_score(y_test, xtre_probs)
stack_auc = roc_auc_score(y_test, stack_probs)

print('RF: AUROC = %.3f' % (rf_auc))
print('LR: AUROC = %.3f' % (lr_auc))
#print('LGBM: AUROC = %.3f' % (lgbm_auc))
print('Extra Trees: AUROC = %.3f' % (xtre_auc))
print('Stack: AUROC = %.3f' % (stack_auc))


rf_fpr, rf_tpr, _ = roc_curve(y_test, rf_probs)
lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
#lgbm_fpr, lgbm_tpr, _ = roc_curve(y_test, lgbm_probs)
xtre_fpr, xtre_tpr, _ = roc_curve(y_test, xtre_probs)
stack_fpr, stack_tpr, _ = roc_curve(y_test, stack_probs)

plt.plot([0, 1], [0, 1], linestyle="--", lw=2, color="r", label="Random Classifier", alpha=0.8)
plt.plot(stack_fpr, stack_tpr, marker='.', label='Stacking (AUROC = %0.3f)' % stack_auc)
plt.plot(xtre_fpr, xtre_tpr, marker='.', label='Extra Trees (AUROC = %0.3f)' % xtre_auc)
#plt.plot(lgbm_fpr, lgbm_tpr, marker='.', label='Light GBM (AUROC = %0.3f)' % lgbm_auc)
plt.plot(rf_fpr, rf_tpr, marker='.', label='Random Forest (AUROC = %0.3f)' % rf_auc)
plt.plot(lr_fpr, lr_tpr, marker='.', label='Logistic Regression (AUROC = %0.3f)' % lr_auc)

# Title
plt.title('ROCAUC Plot')
# Axis labels
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# Show legend
plt.legend() # 
# Show plot
plt.show()