from __PythonScripts.pilot_stats import *
import pingouin
from statsmodels.stats.anova import AnovaRM
from statsmodels.formula.api import ols
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import AnovaRM
from scipy import stats

###########################################
# Running repeated measures ANOVA with group means
##########################################

subER = []
subKA = []
subRT = []
subMU = []
subSNR = []
subPT = []
subSUB = []
subDI = []
subAbsER = []

sub_ID = np.arange(len(data_files))
subTrials = int(data.shape[1] / len(sub_ID))  # 640 trials per each of 16 patients
for g, z in enumerate(sub_ID):  # subjects
    subInd = np.arange(subTrials) + subTrials * g
    for j, y in enumerate(propVal):  # SNR
        # for i, x in enumerate(np.delete(durVal.copy(),[1,2],0)):  # presentation duration, sans 58 and 67
        for i, x in enumerate(durVal):  # presentation duration

            overlap_SNR_PT_SUB = list(set(durInd[x][0]) & set(propInd[y][0]) & set(subInd))

            subSUB.append(z)  # subject
            subSNR.append(y)  # SNR
            subPT.append(x)  # PT

            subER.append(np.nanmean(
                signed_err(est_mu[overlap_SNR_PT_SUB], res_mu[overlap_SNR_PT_SUB])))  # error (absolute/signed)
            subAbsER.append(np.nanmean(abs_err(est_mu[overlap_SNR_PT_SUB], res_mu[overlap_SNR_PT_SUB])))
            subKA.append(np.nanmean(est_kappa[overlap_SNR_PT_SUB]))  # kappa
            subRT.append(np.nanmean(keyRT[overlap_SNR_PT_SUB]))  # RT
            subMU.append(np.nanmean(est_mu[overlap_SNR_PT_SUB]))  # mu

d_mean = {'PT': subPT,
          'Sub': subSUB,
          'SNR': subSNR,
          'Error': subER,
          'AbsError': subAbsER,
          'RT': subRT,
          'Kappa': subKA,
          'Mu': subMU
          }

df_mean = pd.DataFrame(data=d_mean)
np.isnan(df_mean).sum()

hiSNR = []  # averaging, per patient and SNR
loSNR = []

rmaPTER = []  # averaging, per patient and PT
rmaAbsPTER = []
rmaSub = []
rmaRT = []
rmaPT = []

for j, y in enumerate(np.unique(subSUB)):
    loN = list(set(np.where(df_mean['SNR'] == 0)[0]) & set(np.where(df_mean['Sub'] == y)[0]))  # noise
    hiN = list(set(np.where(df_mean['SNR'] == 0.5)[0]) & set(np.where(df_mean['Sub'] == y)[0]))
    loSNR.append(df_mean['AbsError'][loN].mean())
    hiSNR.append(df_mean['AbsError'][hiN].mean())

    for i, x in enumerate(np.unique(subPT)):
        uniPT = list(set(np.where(df_mean['PT'] == x)[0]) & set(np.where(df_mean['Sub'] == y)[0]))  # unique PT
        rmaAbsPTER.append(np.nanmean(df_mean['AbsError'][uniPT]))  # absError
        rmaPTER.append(np.nanmean(df_mean['Error'][uniPT]))  # error
        rmaRT.append(np.nanmean(df_mean['RT'][uniPT]))  # RT
        rmaSub.append(y)  # sub
        rmaPT.append(x)  # PT

d2 = {'PT': rmaPT,
      'Sub': rmaSub,
      'Error': rmaPTER,
      'AbsError': rmaAbsPTER,
      'RT': rmaRT
      }

df_PT = pd.DataFrame(data=d2)
df_PT = df_PT[df_PT.AbsError.notnull()]  # no nan
assert (df_PT.PT.isnull().sum() == 0)

df_mean_nn = df_mean[df_mean.AbsError.notnull()]  # dropping null values
####################################
# # Running Statistical Tests
######################################

# t-test for comparison to Sven's analysis
ttestSNR = pingouin.ttest(loSNR, hiSNR, paired=True)  # correction='auto'

# rm_anova for SNR on Error
rm_SNR = pingouin.rm_anova(data=df_mean_nn, dv='AbsError', within=['SNR'], subject='Sub')
print(rm_SNR)

# # MLM for SNR on Error
# mlm_SNR = smf.mixedlm("AbsError ~ SNR", df_mean_nn, groups=df_mean_nn["Sub"])
# mdf_SNR = mlm_SNR.fit()
# print(mdf_SNR.summary())
#
# A = np.identity(len(mdf_SNR.params))
# A = A[1:,:]
# print(mdf_SNR.f_test(A))

# MLM for PT on Error
mlm_PT = smf.mixedlm("AbsError ~ PT", df_PT, groups=df_PT["Sub"])
mdf_PT = mlm_PT.fit()
print(mdf_PT.summary())

A = np.identity(len(mdf_PT.params))
A = A[1:, :]
print(mdf_PT.f_test(A))

# rm_anova for SNR on RT
rm_SNR = pingouin.rm_anova(data=df_mean_nn, dv='RT', within=['SNR'], subject='Sub')
print(rm_SNR)

# MLM for PT on RT
mlm_PT = smf.mixedlm("RT ~ PT", df_PT, groups=df_PT["Sub"])
mdf_PT = mlm_PT.fit()
print(mdf_PT.summary())

A = np.identity(len(mdf_PT.params))
A = A[1:, :]
print(mdf_PT.f_test(A))


# rm_PT = pingouin.rm_anova(data=df_PT, dv='AbsError', within=['PT'],
#                           subject='Sub')  # no implementation for unbalanced classes in rm_anova

# # testing for sphericity with mauchly's sphericity
# spherSNR = pingouin.sphericity(data=df_mean_nn, dv='Error', within='SNR',
#                                subject='Sub')  # sphericity necessarily met with 2 levels
# spherER = pingouin.sphericity(data=df_mean_nn, dv='Error', within='PT',
#                               subject='Sub')  # big p-value indicates no violation

# # testing for sphericity of interaction
# # (and calculating Greenhouse-Geisser epsilon internally for correction)
# spherInter = pingouin.sphericity(data=df_mean, dv='Error', within=['SNR', 'PT'], subject='Sub')

# # # testing two-way RM ANOVA
# rm_SNRxPT = pingouin.rm_anova(data=df_mean_nn, dv='AbsError', within=['SNR', 'PT'], subject='Sub')

#############################
# Running statistical tests with individual trials
#############################

def rep_test(name, DV, IV, test):
    """Function to report statistics test results"""
    print(f'{name} test\nDifferences in {IV} across {DV}...\nt:{test[0]:.4}, p:{test[1]:.4}\n')


allSub = np.repeat(sub_ID, 640)

d = {'Sub': allSub, 'PT': vizDur, 'SNR': propmix, 'Error': allsignedER, 'AbsError': allER, 'RT': keyRT,
     'Directions': directions, 'Kappa': est_kappa,
     'Mu': est_mu}
df = pd.DataFrame(data=d)
# df = df[df.AbsError.notnull()]  # no nan

# rm_anova for Directions on Error
spherDI = pingouin.sphericity(data=df, dv='AbsError', within='Directions',
                              subject='Sub')  # big p-value indicates no violation
rm_direc = pingouin.rm_anova(data=df, dv='AbsError', within='Directions', subject='Sub')
print(rm_direc)

# rm_anova for Directions on RT
spherDI = pingouin.sphericity(data=df, dv='RT', within='Directions',
                              subject='Sub')  # big p-value indicates no violation
rm_direc = pingouin.rm_anova(data=df, dv='RT', within='Directions', subject='Sub')
print(rm_direc)
#
# # rm Anova with statsmodel -- same results
# rm_direc = AnovaRM(df,'RT','Sub', ['Directions'], aggregate_func='mean')
# rm_fit = rm_direc.fit()
# print(rm_fit.summary())

# # HOMOSCEDACITY TESTS FIRST
#
# # levene's for PT
# def homo_PT(signed_trialERxPT):
#     signed_trialERxPT_levene = stats.levene(signed_trialERxPT[0],signed_trialERxPT[1], signed_trialERxPT[2],
#                                                   signed_trialERxPT[3], signed_trialERxPT[4], signed_trialERxPT[5],
#                                                   signed_trialERxPT[6], signed_trialERxPT[7], signed_trialERxPT[8]) # testing for homoscedascity before ANOVA
#
#     rep_test('Homoscedasticity','error','presentation time',signed_trialERxPT_levene)
#
# homo_PT(signed_trialRTxPT)
# homo_PT(signed_trialERxPT)
#
# # levene's for oblique effect
# signedtrialERxCard_levene = stats.levene(allsignedER[cardinalTrials], allsignedER[obliqueTrials], allsignedER[otherTrials])
# signedtrialRTxCard_levene = stats.levene(keyRT[cardinalTrials], keyRT[obliqueTrials], keyRT[otherTrials])
# rep_test('Homoscedascity','error','directions', signedtrialERxCard_levene)
# rep_test('Homoscedascity','error','directions', signedtrialRTxCard_levene)
#
#
# # ANOVAS NEXT
#
# # ANOVAs for SNR
# signedERxSNR_anova = stats.f_oneway(signed_err(est_mu, res_mu)[loSNR], signed_err(est_mu, res_mu)[hiSNR])
# rep_test('Anova','error','SNR', signedERxSNR_anova)
#
# # ANOVAs for PT
# signedERxPT_anova = stats.f_oneway(signed_trialERxPT[0], signed_trialERxPT[1], signed_trialERxPT[2],
#                                               signed_trialERxPT[3], signed_trialERxPT[4], signed_trialERxPT[5],
#                                               signed_trialERxPT[6], signed_trialERxPT[7], signed_trialERxPT[8])  # Does this violate homoscedascity? (std of each group is equal)
# rep_test('ANOVA','error','presentation time', signedERxPT_anova)
#
# # ANOVAs for oblique effect
# signedERxCard_anova = stats.f_oneway(allsignedER[cardinalTrials], allsignedER[obliqueTrials], allsignedER[otherTrials])
# signedRTxCard_anova = stats.f_oneway(keyRT[cardinalTrials], keyRT[obliqueTrials], keyRT[otherTrials])
# rep_test('ANOVA','error','cardinal vs. oblique vs. other directions',signedERxCard_anova)
# rep_test('ANOVA','RT','cardinal vs. oblique vs. other directions',signedRTxCard_anova)
#
#
# # TWO WAY ANOVAS
# # credit: https://pythonfordatascience.org/anova-2-way-n-way/#test
# # Explanation of Type 1/2/3 SS here: https://mcfromnz.wordpress.com/2011/03/02/anova-type-iiiiii-ss-explained/
#
# # Interaction models first, type 3 SS
# model = ols('Error ~ C(PT)*C(SNR)', df).fit()
# print(f"Overall model F({model.df_model: .0f},{model.df_resid: .0f}) = {model.fvalue: .3f}, p = {model.f_pvalue: .4f}") # testing if model is overall significant
# model.summary()
# res = sm.stats.anova_lm(model, typ= 3) # type 3 to test for interactions first, then if not significant, type 2 to test for main effects
# res
#
# model2 = ols('RT ~ C(PT)*C(SNR)', df).fit()
# print(f"Overall model F({model2.df_model: .0f},{model2.df_resid: .0f}) = {model2.fvalue: .3f}, p = {model2.f_pvalue: .4f}") # testing if model is overall significant
# model2.summary()
# res2 = sm.stats.anova_lm(model2, typ= 3) # Creates the ANOVA table
# res2
#
# # Main effect model for IVs with non-significant interactions
# model3 = ols('RT ~ C(PT) + C(SNR)', df).fit()
# print(f"Overall model F({model3.df_model: .0f},{model3.df_resid: .0f}) = {model3.fvalue: .3f}, p = {model3.f_pvalue: .4f}") # testing if model is overall significant
# model3.summary()
# res3 = sm.stats.anova_lm(model3, typ= 2) # Creates the ANOVA table
# res3
#
# # interaction of direction and SNR
# model4 = ols('RT ~ C(Directions)*C(SNR)', df).fit()
# print(f"Overall model F({model4.df_model: .0f},{model4.df_resid: .0f}) = {model4.fvalue: .3f}, p = {model4.f_pvalue: .4f}") # testing if model is overall significant
# model4.summary()
# res4 = sm.stats.anova_lm(model4, typ= 3) # Creates the ANOVA table
# res4
#
# # model4 = ols('Error ~ C(PT) + C(SNR)', df).fit()
# # print(f"Overall model F({model4.df_model: .0f},{model4.df_resid: .0f}) = {model4.fvalue: .3f}, p = {model4.f_pvalue: .4f}") # testing if model is overall significant
# # model4.summary()
# # res4 = sm.stats.anova_lm(model4, typ= 2) # Creates the ANOVA table
# # res4
#
# # # ANCOVA
# # model3 = ols('Error ~ C(Kappa)', df).fit()
# # model3.summary()
# # res3 = sm.stats.anova_lm(model3, typ= 2) # Creates the ANOVA table
# # res3
# #
# # model4 = ols('Error ~ C(Directions)', df).fit()
# # model4.summary()
# # res4 = sm.stats.anova_lm(model4, typ= 2) # Creates the ANOVA table
# # res4
# #
# # model5 = ols('Error ~ C(Mu)', df).fit()
# # model5.summary()
# # res5 = sm.stats.anova_lm(model5, typ= 2) # Creates the ANOVA table
# # res5
#
#
# # FINALLY T-TESTs
#
# # for direction
# signedERxCOb_ttest = stats.ttest_ind(allsignedER[cardinalTrials], allsignedER[obliqueTrials])  # oblique peforms worse, also against non-cardinal, non-oblique trials
# signedERxOtOb_ttest = stats.ttest_ind(allsignedER[otherTrials], allsignedER[obliqueTrials])
# signedERxOtC_ttest = stats.ttest_ind(allsignedER[otherTrials], allsignedER[cardinalTrials])
# rep_test('T-test','error','cardinal vs. oblique direction',signedERxCOb_ttest)
# rep_test('T-test','error','other vs. oblique direction',signedERxOtOb_ttest)
# rep_test('T-test','error','other vs. cardinal direction',signedERxOtC_ttest)
#
# # testing oblique effect in lo vs. hi SNR
# hiOb = list(set(obliqueTrials) & set(hiSNR))
# hiCa = list(set(cardinalTrials) & set(hiSNR))
# loOb = list(set(obliqueTrials) & set(loSNR))
# loCa = list(set(cardinalTrials) & set(loSNR))
#
# signedERxDirecHi_ttest = stats.ttest_ind(allsignedER[hiCa], allsignedER[hiOb])
# rep_test('T-test','error','high SNR (oblique vs. cardinal directions)', signedERxDirecHi_ttest)
#
# signedERxDirecLo_ttest = stats.ttest_ind(allsignedER[loCa], allsignedER[loOb])
# rep_test('T-test','error','low SNR (oblique vs. cardinal directions)', signedERxDirecLo_ttest)
#
# # for SNR
# signedERxSNR_ttest = stats.ttest_ind(signed_err(est_mu, res_mu)[loSNR], signed_err(est_mu, res_mu)[hiSNR]) # no sig diff
# rep_test('T-test','error','SNR', signedERxSNR_ttest)
# signedRTxSNR_ttest = stats.ttest_ind(keyRT[loSNR], keyRT[hiSNR])  # no sig diff
# rep_test('T-test','RT','SNR', signedRTxSNR_ttest)
